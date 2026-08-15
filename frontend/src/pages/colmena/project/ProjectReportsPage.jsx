import { useState } from 'react';
import { useParams } from 'react-router-dom';
import { useMutation, useQuery } from '@tanstack/react-query';
import { AlertCircle, CheckCircle2, Download, FileText, ShieldCheck } from 'lucide-react';

import { useAuth } from '../../../auth/AuthContext.jsx';
import { useActiveProject } from '../../../hooks/useActiveProject.js';
import { getProject } from '../../../api/projects.js';
import { getStudy } from '../../../api/studies.js';
import { getCensopasReadiness } from '../../../api/instruments.js';
import { createReport, createReportTemplate, getReport, getReportDownloadUrl } from '../../../api/reports.js';

import { PageHeader } from '../../../components/layout/PageHeader.jsx';
import { Card } from '../../../components/ui/Card.jsx';
import { Button } from '../../../components/ui/Button.jsx';
import { PrimaryAction } from '../../../components/ui/PrimaryAction.jsx';
import { StatusPill } from '../../../components/ui/StatusPill.jsx';
import { EmptyState } from '../../../components/ui/EmptyState.jsx';
import { LoadingState } from '../../../components/ui/LoadingState.jsx';
import FormField from '../../../components/ui/FormField.jsx';
import { ProjectMissingState } from '../../../components/colmena/ProjectMissingState.jsx';
import StudySelector from '../../../components/colmena/StudySelector.jsx';
import ReportWizardSteps from '../../../components/colmena/reports/ReportWizardSteps.jsx';

const SECTIONS = [
  { key: 'portada', label: 'Portada' },
  { key: 'ficha_tecnica', label: 'Ficha técnica' },
  { key: 'participacion_privacidad', label: 'Participación y privacidad' },
  { key: 'resultados_globales', label: 'Resultados globales' },
  { key: 'dimensiones', label: 'Dimensiones' },
  { key: 'subdimensiones', label: 'Subdimensiones' },
  { key: 'unidades_seguras', label: 'Unidades seguras' },
  { key: 'variables_descriptivas', label: 'Variables descriptivas' },
  { key: 'hallazgos_premium', label: 'Hallazgos premium' },
  { key: 'plan_accion', label: 'Plan de acción' },
  { key: 'anexos', label: 'Anexos' },
  { key: 'trazabilidad', label: 'Trazabilidad' },
];

export default function ProjectReportsPage() {
  const { projectId } = useParams();
  const { user } = useAuth();
  useActiveProject(projectId);

  const [step, setStep] = useState(0);
  const [studyId, setStudyId] = useState(null);
  const [templateName, setTemplateName] = useState('Reporte estándar');
  const [template, setTemplate] = useState(null);
  const [sections, setSections] = useState([]);
  const [report, setReport] = useState(null);
  const [reportMode, setReportMode] = useState('PROVISIONAL');
  const [outputFormat, setOutputFormat] = useState('DOCX');

  const { data: project, isLoading: isLoadingProject } = useQuery({
    queryKey: ['project', projectId],
    queryFn: () => getProject(projectId),
  });

  const { data: study } = useQuery({
    queryKey: ['study', studyId],
    queryFn: () => getStudy(studyId),
    enabled: Boolean(studyId),
  });

  const { data: readiness, isFetching: isLoadingReadiness } = useQuery({
    queryKey: ['censopas-readiness', study?.instrument_version_id],
    queryFn: () => getCensopasReadiness(study.instrument_version_id),
    enabled: Boolean(study?.instrument_version_id),
  });

  const createTemplateMutation = useMutation({
    mutationFn: () => createReportTemplate({
      name: templateName,
      report_type: 'CENSOPAS_COPSOQ',
      instrument_version_id: study?.instrument_version_id,
      template_config: { methodology: 'CENSOPAS_COPSOQ' },
    }),
    onSuccess: (data) => {
      setTemplate(data);
      setStep(2);
    },
  });

  const createReportMutation = useMutation({
    mutationFn: () =>
      createReport(studyId, { report_template_id: template.id, output_format: outputFormat, requested_by_user_id: user.id, report_mode: reportMode, sections }),
    onSuccess: (data) => setReport(data),
  });

  const { data: reportStatus } = useQuery({
    queryKey: ['report', report?.id],
    queryFn: () => getReport(report.id),
    enabled: Boolean(report?.id),
    refetchInterval: (query) => (query.state.data && ['COMPLETED', 'FAILED'].includes(query.state.data.status) ? false : 1500),
  });

  const toggleSection = (key) => {
    setSections((prev) => (prev.includes(key) ? prev.filter((s) => s !== key) : [...prev, key]));
  };

  if (isLoadingProject) return <LoadingState label="Cargando..." />;
  if (!project) return <ProjectMissingState />;

  return (
    <div className="colmena-page">
      <PageHeader eyebrow="Reportes" title={project.name} description="Genera reportes estructurados a partir de los análisis del estudio." />

      <Card>
        <ReportWizardSteps current={step} />
      </Card>

      <Card>
        {step === 0 ? (
          <div className="flex flex-col gap-4">
            <StudySelector projectId={projectId} studyId={studyId} onStudyChange={setStudyId} />
            {studyId ? (
              <div className="rounded-2xl border border-border bg-surface p-4">
                <div className="mb-3 flex flex-wrap items-center justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <ShieldCheck size={18} className="text-turquoise" />
                    <div>
                      <p className="text-sm font-semibold text-dark">Preparación CENSOPAS-COPSOQ</p>
                      <p className="text-xs text-muted">
                        {isLoadingReadiness ? 'Verificando estructura…' : 'Versión ' + (readiness?.version_kind || 'desconocida')}
                      </p>
                    </div>
                  </div>
                  {readiness ? (
                    <span className={'colmena-badge ' + (readiness.ready_for_scoring ? 'bg-turquoise/10 text-turquoise' : 'bg-danger/10 text-danger')}>
                      {readiness.ready_for_scoring ? 'Listo para scoring' : 'Configuración incompleta'}
                    </span>
                  ) : null}
                </div>
                {readiness ? (
                  <>
                    <div className="grid gap-2 sm:grid-cols-4">
                      {[
                        ['Preguntas', 'questions'],
                        ['Puntuables', 'scored'],
                        ['Dimensiones', 'dimensions'],
                        ['Subdimensiones', 'subdimensions'],
                      ].map(([label, key]) => {
                        const matches = readiness.actual[key] === readiness.expected[key];
                        return (
                          <div key={key} className="rounded-xl border border-border bg-background/60 p-3">
                            <p className="text-[11px] font-semibold uppercase tracking-wide text-muted">{label}</p>
                            <p className={'mt-1 text-sm font-bold ' + (matches ? 'text-dark' : 'text-danger')}>
                              {readiness.actual[key] ?? 0} / {readiness.expected[key] ?? '—'}
                            </p>
                          </div>
                        );
                      })}
                    </div>
                    <div className="mt-3 flex items-start gap-2 rounded-xl border border-border px-3 py-2">
                      {readiness.ready_for_official_reporting ? (
                        <CheckCircle2 size={16} className="mt-0.5 shrink-0 text-turquoise" />
                      ) : (
                        <AlertCircle size={16} className="mt-0.5 shrink-0 text-amber" />
                      )}
                      <p className="text-xs text-muted">
                        {readiness.ready_for_official_reporting
                          ? 'Equivalencia oficial habilitada y baremo completo.'
                          : 'La salida oficial está bloqueada. Puedes generar un documento provisional claramente etiquetado.'}
                      </p>
                    </div>
                  </>
                ) : null}
              </div>
            ) : null}
            <Button variant="primary" size="sm" onClick={() => setStep(1)} disabled={!studyId} className="w-40">
              Continuar
            </Button>
          </div>
        ) : null}

        {step === 1 ? (
          <div className="flex flex-col gap-4">
            <FormField label="Nombre de la plantilla" value={templateName} onChange={(event) => setTemplateName(event.target.value)} />
            <div className="flex gap-3">
              <Button variant="secondary" size="sm" onClick={() => setStep(0)}>
                Atrás
              </Button>
              <Button variant="primary" size="sm" onClick={() => createTemplateMutation.mutate()} loading={createTemplateMutation.isPending}>
                Crear plantilla y continuar
              </Button>
            </div>
          </div>
        ) : null}

        {step === 2 ? (
          <div className="flex flex-col gap-4">
            <p className="colmena-label">Secciones a incluir</p>
            <div className="flex flex-wrap gap-2">
              {SECTIONS.map((section) => (
                <button
                  key={section.key}
                  type="button"
                  onClick={() => toggleSection(section.key)}
                  className={`colmena-badge cursor-pointer ${sections.includes(section.key) ? 'bg-amber text-white' : 'bg-amber/10 text-yellowDark'}`}
                >
                  {section.label}
                </button>
              ))}
            </div>
            <div className="flex gap-3">
              <Button variant="secondary" size="sm" onClick={() => setStep(1)}>
                Atrás
              </Button>
              <Button variant="primary" size="sm" onClick={() => setStep(3)} disabled={sections.length === 0}>
                Continuar
              </Button>
            </div>
          </div>
        ) : null}

        {step === 3 ? (
          <div className="flex flex-col gap-4">
            <p className="text-sm text-muted">
              Este estudio requiere un mínimo de <strong className="text-dark">{study?.min_publishable_n ?? '—'}</strong> respuestas
              válidas por celda para publicar resultados desagregados. El backend aplica esta regla de privacidad al generar el
              reporte — el frontend no la calcula ni la puede saltar.
            </p>
            <div className="flex gap-3">
              <Button variant="secondary" size="sm" onClick={() => setStep(2)}>
                Atrás
              </Button>
              <Button variant="primary" size="sm" onClick={() => setStep(4)}>
                Continuar
              </Button>
            </div>
          </div>
        ) : null}

        {step === 4 ? (
          <div className="flex flex-col gap-4">
            {!report ? (
              <>
                <p className="text-sm text-muted">
                  Elige el estatus metodológico del documento. El backend volverá a validar readiness antes de crear una salida oficial.
                </p>
                <div className="grid gap-3 sm:grid-cols-2">
                  <button
                    type="button"
                    onClick={() => setReportMode('PROVISIONAL')}
                    className={'rounded-xl border p-4 text-left ' + (reportMode === 'PROVISIONAL' ? 'border-amber bg-amber/5' : 'border-border bg-surface')}
                  >
                    <FileText size={18} className="mb-2 text-amber" />
                    <span className="block text-sm font-semibold text-dark">Reporte provisional</span>
                    <span className="mt-1 block text-xs text-muted">Disponible para pruebas; se rotula sin equivalencia oficial.</span>
                  </button>
                  <button
                    type="button"
                    disabled={!readiness?.ready_for_official_reporting}
                    onClick={() => setReportMode('OFFICIAL')}
                    className={'rounded-xl border p-4 text-left ' + (reportMode === 'OFFICIAL' ? 'border-turquoise bg-turquoise/5' : 'border-border bg-surface') + ' disabled:cursor-not-allowed disabled:opacity-50'}
                  >
                    <ShieldCheck size={18} className="mb-2 text-turquoise" />
                    <span className="block text-sm font-semibold text-dark">Reporte oficial</span>
                    <span className="mt-1 block text-xs text-muted">Requiere manifiesto, scoring, baremo y equivalencia habilitados.</span>
                  </button>
                </div>
                <div className="max-w-xs">
                  <label className="colmena-label mb-2 block" htmlFor="report-output-format">Formato de salida</label>
                  <select
                    id="report-output-format"
                    className="colmena-input w-full"
                    value={outputFormat}
                    onChange={(event) => setOutputFormat(event.target.value)}
                  >
                    <option value="DOCX">Word (.docx)</option>
                    <option value="PDF">PDF (.pdf)</option>
                  </select>
                </div>
                <div className="flex gap-3">
                  <Button variant="secondary" size="sm" onClick={() => setStep(3)}>
                    Atrás
                  </Button>
                  <PrimaryAction onClick={() => createReportMutation.mutate()} loading={createReportMutation.isPending}>
                    <FileText size={16} className="mr-1" />
                    Generar {reportMode === 'OFFICIAL' ? 'reporte oficial' : 'reporte provisional'}
                  </PrimaryAction>
                </div>
                {createReportMutation.isError ? <p className="text-sm font-medium text-danger">No pudimos generar el reporte.</p> : null}
              </>
            ) : (
              <div className="flex flex-col gap-3">
                <div className="flex items-center gap-2">
                  <StatusPill label={reportStatus?.status || report.status} tone="report" />
                  {reportStatus?.error_message ? <span className="text-sm text-danger">{reportStatus.error_message}</span> : null}
                </div>
                {reportStatus?.status === 'COMPLETED' ? (
                  <a href={getReportDownloadUrl(report.id)} target="_blank" rel="noreferrer" className="colmena-button-primary w-56">
                    <Download size={16} className="mr-2" />
                    Descargar {reportStatus?.output_format === 'PDF' ? 'PDF' : 'Word'}
                  </a>
                ) : (
                  <LoadingState label="Generando..." />
                )}
              </div>
            )}
          </div>
        ) : null}
      </Card>

      {!studyId && step === 0 ? (
        <Card>
          <EmptyState title="Elige un estudio para empezar." description="El wizard te guía por 5 pasos hasta descargar el reporte." />
        </Card>
      ) : null}
    </div>
  );
}
