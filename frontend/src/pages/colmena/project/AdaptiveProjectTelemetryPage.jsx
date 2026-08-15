import { useEffect, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Pause, Play, RefreshCcw } from 'lucide-react';
import { useParams } from 'react-router-dom';

import { getProject } from '../../../api/projects.js';
import {
  getResponseDescriptives,
  getResultsOverview,
  getWideDataset,
  listStudies,
} from '../../../api/studies.js';
import { getProjectTelemetry } from '../../../api/telemetry.js';
import { useActiveProject } from '../../../hooks/useActiveProject.js';

import { PageHeader } from '../../../components/layout/PageHeader.jsx';
import { Button } from '../../../components/ui/Button.jsx';
import { Card } from '../../../components/ui/Card.jsx';
import { EmptyState } from '../../../components/ui/EmptyState.jsx';
import { ErrorState } from '../../../components/ui/ErrorState.jsx';
import { LoadingState } from '../../../components/ui/LoadingState.jsx';
import { ProjectMissingState } from '../../../components/colmena/ProjectMissingState.jsx';
import ResponseDistributionsTab from '../../../components/colmena/telemetry/ResponseDistributionsTab.jsx';
import ResponseMatrixTab from '../../../components/colmena/telemetry/ResponseMatrixTab.jsx';
import TelemetryComparisonsTab from '../../../components/colmena/telemetry/TelemetryComparisonsTab.jsx';
import TelemetrySummaryTab from '../../../components/colmena/telemetry/TelemetrySummaryTab.jsx';

const TABS = [
  { key: 'summary', label: 'Resumen' },
  { key: 'distributions', label: 'Distribuciones' },
  { key: 'comparisons', label: 'Comparaciones' },
  { key: 'responses', label: 'Base de respuestas' },
];

function usePageVisibility() {
  const [visible, setVisible] = useState(() => document.visibilityState === 'visible');
  useEffect(() => {
    const update = () => setVisible(document.visibilityState === 'visible');
    document.addEventListener('visibilitychange', update);
    return () => document.removeEventListener('visibilitychange', update);
  }, []);
  return visible;
}

export default function AdaptiveProjectTelemetryPage() {
  const { projectId } = useParams();
  useActiveProject(projectId);
  const [tab, setTab] = useState('summary');
  const [studyId, setStudyId] = useState(null);
  const [paused, setPaused] = useState(false);
  const pageVisible = usePageVisibility();
  const refetchInterval = !paused && pageVisible ? 15000 : false;

  const projectQuery = useQuery({
    queryKey: ['project', projectId],
    queryFn: () => getProject(projectId),
  });
  const studiesQuery = useQuery({
    queryKey: ['studies', projectId],
    queryFn: () => listStudies(projectId, { page: 1, pageSize: 100 }),
    enabled: Boolean(projectId),
  });
  const studies = studiesQuery.data?.items || [];

  useEffect(() => {
    if (!studyId && studies.length) setStudyId(studies[0].id);
    if (studyId && studies.length && !studies.some((study) => study.id === studyId)) {
      setStudyId(studies[0].id);
    }
  }, [studies, studyId]);

  const telemetryQuery = useQuery({
    queryKey: ['projectTelemetry', projectId],
    queryFn: () => getProjectTelemetry(projectId),
    enabled: Boolean(projectId),
    refetchInterval,
    refetchIntervalInBackground: false,
  });
  const descriptivesQuery = useQuery({
    queryKey: ['responseDescriptives', studyId],
    queryFn: () => getResponseDescriptives(studyId),
    enabled: Boolean(studyId),
    refetchInterval,
    refetchIntervalInBackground: false,
  });
  const overviewQuery = useQuery({
    queryKey: ['resultsOverview', studyId],
    queryFn: () => getResultsOverview(studyId),
    enabled: Boolean(studyId),
    refetchInterval,
    refetchIntervalInBackground: false,
  });
  const datasetQuery = useQuery({
    queryKey: ['wideDataset', studyId],
    queryFn: () => getWideDataset(studyId),
    enabled: Boolean(studyId) && tab === 'responses',
    refetchInterval: tab === 'responses' ? refetchInterval : false,
    refetchIntervalInBackground: false,
  });

  const selectedTelemetry = (telemetryQuery.data?.studies || []).find((study) => study.study_id === studyId);
  const isRefreshing = telemetryQuery.isFetching || descriptivesQuery.isFetching || overviewQuery.isFetching || datasetQuery.isFetching;
  const hasDataError = telemetryQuery.isError || descriptivesQuery.isError || overviewQuery.isError || datasetQuery.isError;

  const refresh = () => {
    telemetryQuery.refetch();
    if (studyId) {
      descriptivesQuery.refetch();
      overviewQuery.refetch();
      if (tab === 'responses') datasetQuery.refetch();
    }
  };

  if (projectQuery.isLoading) return <LoadingState label="Cargando proyecto…" />;
  if (!projectQuery.data) return <ProjectMissingState />;

  return (
    <div className="colmena-page">
      <PageHeader
        eyebrow="Telemetría"
        title={projectQuery.data.name}
        description="Participación, distribuciones, comparaciones y respuestas válidas en un solo dashboard."
        actions={(
          <>
            <Button onClick={() => setPaused((value) => !value)} size="sm" type="button" variant="secondary">
              {paused ? <Play size={14} /> : <Pause size={14} />}
              {paused ? 'Reanudar' : 'Pausar'}
            </Button>
            <Button disabled={isRefreshing} onClick={refresh} size="sm" type="button" variant="secondary">
              <RefreshCcw className={isRefreshing ? 'animate-spin' : ''} size={14} />
              Actualizar
            </Button>
          </>
        )}
      />

      <Card padding="compact">
        <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
          <label className="flex min-w-0 flex-col gap-1.5 sm:flex-row sm:items-center">
            <span className="colmena-label shrink-0">Aplicación / estudio</span>
            <select
              className="colmena-input min-w-0 sm:min-w-[280px]"
              onChange={(event) => setStudyId(event.target.value ? Number(event.target.value) : null)}
              value={studyId || ''}
            >
              <option value="">Selecciona un estudio</option>
              {studies.map((study) => <option key={study.id} value={study.id}>{study.name} ({study.status})</option>)}
            </select>
          </label>
          <div className="flex items-center gap-2 text-[11px] text-muted">
            <span className={`h-2 w-2 rounded-full ${paused || !pageVisible ? 'bg-warning' : 'bg-success'}`} />
            {paused ? 'Actualización pausada' : !pageVisible ? 'En espera: página no visible' : 'Actualización automática cada 15 s'}
          </div>
        </div>
      </Card>

      <div className="flex gap-1 overflow-x-auto border-b border-border/70 pb-px">
        {TABS.map((item) => (
          <button
            key={item.key}
            className={`colmena-pill-tab shrink-0 ${tab === item.key ? 'active' : ''}`}
            onClick={() => setTab(item.key)}
            type="button"
          >
            {item.label}
          </button>
        ))}
      </div>

      {hasDataError ? (
        <ErrorState
          message="Conservamos la última información disponible. Usa Actualizar para volver a intentar."
          title="No se pudo actualizar todo el dashboard"
        />
      ) : null}

      {!studyId && !studiesQuery.isLoading ? (
        <Card>
          <EmptyState title="Todavía no hay aplicaciones" description="Crea un estudio para comenzar a recibir telemetría." />
        </Card>
      ) : null}

      {studyId && tab === 'summary' ? (
        <TelemetrySummaryTab
          isLoading={telemetryQuery.isLoading}
          overview={overviewQuery.data}
          telemetry={selectedTelemetry}
        />
      ) : null}
      {studyId && tab === 'distributions' ? (
        <ResponseDistributionsTab
          descriptives={descriptivesQuery.data}
          isLoading={descriptivesQuery.isLoading}
        />
      ) : null}
      {studyId && tab === 'comparisons' ? (
        <TelemetryComparisonsTab
          descriptives={descriptivesQuery.data}
          overview={overviewQuery.data}
          studyId={studyId}
        />
      ) : null}
      {studyId && tab === 'responses' ? (
        <ResponseMatrixTab
          dataset={datasetQuery.data}
          descriptives={descriptivesQuery.data}
          isLoading={datasetQuery.isLoading}
          studyId={studyId}
        />
      ) : null}
    </div>
  );
}
