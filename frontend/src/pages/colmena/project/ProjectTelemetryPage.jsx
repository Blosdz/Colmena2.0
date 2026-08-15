import { useParams } from 'react-router-dom';
import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { Activity, CheckCircle2, Clock, Users } from 'lucide-react';

import { useActiveProject } from '../../../hooks/useActiveProject.js';
import { getProject } from '../../../api/projects.js';
import { getProjectTelemetry } from '../../../api/telemetry.js';

import { PageHeader } from '../../../components/layout/PageHeader.jsx';
import { Card } from '../../../components/ui/Card.jsx';
import MetricCard from '../../../components/ui/MetricCard.jsx';
import { EmptyState } from '../../../components/ui/EmptyState.jsx';
import { LoadingState } from '../../../components/ui/LoadingState.jsx';
import { ProjectMissingState } from '../../../components/colmena/ProjectMissingState.jsx';
import DimensionDashboardTab from '../../../components/colmena/telemetry/DimensionDashboardTab.jsx';

const TABS = [
  { key: 'resumen', label: 'Resumen' },
  { key: 'dashboard', label: 'Dashboard por dimensión' },
];

function aggregateStudies(studies) {
  const started = studies.reduce((total, study) => total + study.started_count, 0);
  const completed = studies.reduce((total, study) => total + study.completed_count, 0);
  const durationWeight = studies.reduce(
    (total, study) => total + (study.avg_duration_seconds || 0) * study.completed_count,
    0,
  );
  return {
    started,
    completed,
    completionRate: started ? completed / started : null,
    avgDuration: completed ? durationWeight / completed : null,
  };
}

function groupVariables(studies) {
  const groups = new Map();
  studies.forEach((study) => {
    (study.variables || []).forEach((variable) => {
      const key = `${study.instrument_version_id || study.study_id}:${variable.construct_id}`;
      const current = groups.get(key) || {
        variableKey: key,
        code: variable.variable_code,
        name: variable.variable_name,
        role: variable.role,
        applications: 0,
        started: 0,
        answered: 0,
        completed: 0,
      };
      current.applications += 1;
      current.started += variable.sessions_started;
      current.answered += variable.sessions_answered;
      current.completed += variable.sessions_completed;
      groups.set(key, current);
    });
  });
  return [...groups.values()].map((group) => ({
    ...group,
    completionRate: group.started ? group.completed / group.started : null,
  }));
}

export default function ProjectTelemetryPage() {
  const { projectId } = useParams();
  useActiveProject(projectId);
  const [tab, setTab] = useState('resumen');

  const { data: project, isLoading: isLoadingProject } = useQuery({
    queryKey: ['project', projectId],
    queryFn: () => getProject(projectId),
  });

  const { data: telemetry, isLoading } = useQuery({
    queryKey: ['projectTelemetry', projectId],
    queryFn: () => getProjectTelemetry(projectId),
    enabled: Boolean(projectId),
  });

  const studies = telemetry?.studies || [];
  const summary = aggregateStudies(studies);
  const comparison = groupVariables(studies);
  const variableApplications = studies.flatMap((study) =>
    (study.variables || []).map((variable) => ({ ...variable, studyName: study.study_name, studyId: study.study_id })),
  );

  if (isLoadingProject) return <LoadingState label="Cargando..." />;
  if (!project) return <ProjectMissingState />;

  return (
    <div className="colmena-page">
      <PageHeader eyebrow="Telemetría" title={project.name} description="Compara cobertura y finalización entre las variables del proyecto." />

      <div className="flex gap-2 overflow-x-auto">
        {TABS.map((t) => (
          <button key={t.key} type="button" onClick={() => setTab(t.key)} className={`colmena-pill-tab ${tab === t.key ? 'active' : ''}`}>
            {t.label}
          </button>
        ))}
      </div>

      {tab === 'resumen' ? (
        isLoading ? (
          <LoadingState label="Cargando telemetría..." />
        ) : studies.length === 0 ? (
          <Card>
            <EmptyState title="Todavía no hay estudios con telemetría." description="Crea una aplicación, abre su recolección y recibe respuestas.">
              <div className="mx-auto flex h-10 w-11 items-center justify-center rounded-2xl bg-amber/10 text-amber">
                <Activity size={20} />
              </div>
            </EmptyState>
          </Card>
        ) : (
          <>
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-4">
              <MetricCard icon={Users} label="Sesiones iniciadas" value={summary.started} />
              <MetricCard icon={CheckCircle2} label="Completadas" value={summary.completed} />
              <MetricCard
                icon={Activity}
                label="Tasa de finalización"
                value={summary.completionRate !== null ? `${Math.round(summary.completionRate * 100)}%` : '—'}
              />
              <MetricCard
                icon={Clock}
                label="Duración promedio"
                value={summary.avgDuration !== null ? `${Math.round(summary.avgDuration)}s` : '—'}
              />
            </div>

            <Card>
              <p className="mb-1 text-sm font-semibold text-dark">Cobertura por variable</p>
              <p className="mb-4 text-xs text-muted">Una variable se considera completa cuando la sesión contestó todas las preguntas de sus dimensiones.</p>
              {comparison.length ? (
                <div className="h-72 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={comparison}>
                      <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,0.25)" />
                      <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                      <YAxis allowDecimals={false} tick={{ fontSize: 12 }} />
                      <Tooltip />
                      <Legend />
                      <Bar dataKey="started" name="Sesiones" fill="#FDE7AB" radius={[6, 6, 0, 0]} />
                      <Bar dataKey="answered" name="Con alguna respuesta" fill="#F8CA58" radius={[6, 6, 0, 0]} />
                      <Bar dataKey="completed" name="Variable completa" fill="#F5B21A" radius={[6, 6, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              ) : (
                <EmptyState title="Todavía no hay variables medibles" description="Crea variables con dimensiones y preguntas para comparar su cobertura." />
              )}
            </Card>

            <Card padded={false}>
              <div className="border-b border-border px-4 py-3">
                <p className="text-sm font-semibold text-dark">Detalle por aplicación</p>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="bg-surfaceSoft">
                    <tr>
                      {['Variable', 'Rol', 'Estudio', 'Preguntas', 'Sesiones', 'Respondida', 'Completa'].map((label) => (
                        <th key={label} className="px-4 py-3 text-xs font-semibold text-muted">{label}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {variableApplications.map((variable) => (
                      <tr key={`${variable.studyId}:${variable.construct_id}`} className="border-t border-border">
                        <td className="px-4 py-3"><p className="font-medium text-dark">{variable.variable_name}</p><p className="font-mono text-xs text-muted">{variable.variable_code}</p></td>
                        <td className="px-4 py-3 text-xs">{variable.role || '—'}</td>
                        <td className="px-4 py-3 text-dark">{variable.studyName}</td>
                        <td className="px-4 py-3">{variable.question_count}</td>
                        <td className="px-4 py-3">{variable.sessions_started}</td>
                        <td className="px-4 py-3">{variable.sessions_answered}</td>
                        <td className="px-4 py-3">{variable.completion_rate === null ? '—' : `${Math.round(variable.completion_rate * 100)}%`}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </Card>
          </>
        )
      ) : null}

      {tab === 'dashboard' ? <DimensionDashboardTab projectId={projectId} /> : null}
    </div>
  );
}
