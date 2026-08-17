import { useState } from 'react';
import { useParams } from 'react-router-dom';
import { useMutation, useQuery } from '@tanstack/react-query';
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { Activity, AlertTriangle, Clock, Layers, Sparkles, Target, Users } from 'lucide-react';

import { useActiveProject } from '../../../hooks/useActiveProject.js';
import { getProject } from '../../../api/projects.js';
import { getProjectTelemetry } from '../../../api/telemetry.js';
import { getResultsOverview } from '../../../api/studies.js';
import { listVariables } from '../../../api/variables.js';
import { runAnalysis, runSpearmanMatrix } from '../../../api/analytics.js';

import { PageHeader } from '../../../components/layout/PageHeader.jsx';
import { Button } from '../../../components/ui/Button.jsx';
import { Card } from '../../../components/ui/Card.jsx';
import { EmptyState } from '../../../components/ui/EmptyState.jsx';
import { LoadingState } from '../../../components/ui/LoadingState.jsx';
import MetricCard from '../../../components/ui/MetricCard.jsx';
import { Table, TableContainer, Td, THead, Th, Tr } from '../../../components/ui/Table.jsx';
import { ProjectMissingState } from '../../../components/colmena/ProjectMissingState.jsx';
import StudySelector from '../../../components/colmena/StudySelector.jsx';
import { SpearmanMatrix } from '../../../components/colmena/results/SpearmanPanel.jsx';
import { formatNumber, formatPercent } from '../../../utils/format.js';
import { semanticBand, semanticBandColor, semanticBandOrder } from '../../../utils/chartColors.js';
import { dominantBand, unfavorablePct } from '../../../utils/scoringResults.js';
import PriorityBarChart from '../../../components/colmena/results/PriorityBarChart.jsx';

const K_OPTIONS = [2, 3, 4];

function formatDuration(seconds) {
  if (seconds === null || seconds === undefined) return '—';
  const rounded = Math.round(seconds);
  if (rounded < 60) return `${rounded}s`;
  return `${Math.floor(rounded / 60)}m ${rounded % 60}s`;
}

function DimensionDistributionRow({ result }) {
  const bands = [...(result.bands || [])].sort((a, b) => semanticBandOrder(a.label) - semanticBandOrder(b.label));
  return (
    <div className="py-2.5">
      <div className="mb-1.5 flex items-center justify-between gap-3 text-xs">
        <span className="font-semibold text-dark">{result.construct_name}</span>
        <span className="text-muted">n = {result.n_valid}</span>
      </div>
      {result.suppressed ? (
        <div className="flex h-6 items-center justify-center rounded-md bg-surfaceSoft text-[11px] text-muted">
          Suprimido por privacidad
        </div>
      ) : (
        <div className="flex h-6 overflow-hidden rounded-md border border-border">
          {bands.map((band) => (
            <div
              key={band.label}
              className="flex items-center justify-center text-[10px] font-bold text-white"
              style={{ width: `${band.pct || 0}%`, background: band.color_hint || semanticBandColor(band.label) }}
              title={`${band.label}: ${formatPercent(band.pct)}`}
            >
              {(band.pct || 0) >= 12 ? formatPercent(band.pct, { decimals: 0 }) : ''}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function PriorityTable({ rows }) {
  return (
    <TableContainer>
      <Table>
        <THead>
          <Tr>
            <Th>#</Th>
            <Th>Dimensión</Th>
            <Th align="right">n</Th>
            <Th align="right">% desfavorable</Th>
            <Th>Nivel dominante</Th>
          </Tr>
        </THead>
        <tbody>
          {rows.map((result, index) => {
            const dominant = dominantBand(result);
            return (
              <Tr key={result.construct_id}>
                <Td className="font-semibold text-muted">{result.priority_rank ?? index + 1}</Td>
                <Td className="font-medium text-dark">{result.construct_name}</Td>
                <Td align="right">{result.n_valid}</Td>
                <Td align="right" className="font-mono font-semibold text-dark">
                  {formatPercent(unfavorablePct(result), { decimals: 1 })}
                </Td>
                <Td>
                  {dominant ? (
                    <span
                      className="inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-[11px] font-semibold text-white"
                      style={{ background: dominant.color_hint || semanticBandColor(dominant.label) }}
                    >
                      {dominant.label}
                    </span>
                  ) : (
                    '—'
                  )}
                </Td>
              </Tr>
            );
          })}
        </tbody>
      </Table>
    </TableContainer>
  );
}

function SpearmanCard({ studyId }) {
  const [selectedIndex, setSelectedIndex] = useState(0);
  const mutation = useMutation({
    mutationFn: () => runSpearmanMatrix(studyId, { include_points: false }),
    onSuccess: () => setSelectedIndex(0),
    meta: { skipGlobalToast: true },
  });

  return (
    <Card>
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="text-sm font-semibold text-dark">¿Qué dimensiones se mueven juntas?</p>
          <p className="mt-1 text-xs text-muted">Matriz de correlación de Spearman · exploratoria, no causal.</p>
        </div>
        <Button loading={mutation.isPending} onClick={() => mutation.mutate()} size="sm" type="button" variant="secondary">
          <Sparkles size={14} /> Calcular matriz
        </Button>
      </div>
      {mutation.isError ? <p className="mt-3 text-xs font-medium text-danger">{mutation.error?.message}</p> : null}
      {mutation.data ? (
        <div className="mt-4">
          <SpearmanMatrix
            variables={mutation.data.variables}
            cells={mutation.data.cells}
            selectedIndex={selectedIndex}
            onSelect={setSelectedIndex}
          />
          {mutation.data.excluded?.map((message) => (
            <p key={message} className="mt-2 text-xs text-danger">{message}</p>
          ))}
        </div>
      ) : (
        <div className="mt-4 rounded-xl border border-dashed border-border p-5 text-sm text-muted">
          Calcula la matriz para ver qué dimensiones correlacionan entre sí.
        </div>
      )}
    </Card>
  );
}

function SegmentationCard({ studyId, rankableVariables }) {
  const [variableIds, setVariableIds] = useState([]);
  const [k, setK] = useState(3);

  const mutation = useMutation({
    mutationFn: () => runAnalysis('kmeans', studyId, { variable_ids: variableIds, k }),
    meta: { skipGlobalToast: true },
  });

  const toggle = (id) => setVariableIds((prev) => (prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]));

  const result = mutation.data?.results?.[0];
  const clusterData = result?.result_data;

  return (
    <Card>
      <div>
        <p className="text-sm font-semibold text-dark">Segmentos exploratorios</p>
        <p className="mt-1 text-xs text-muted">
          Agrupa patrones parecidos con k-means sobre variables ordinales o de escala. No clasifica ni diagnostica personas.
        </p>
      </div>

      {rankableVariables.length ? (
        <div className="mt-3">
          <p className="colmena-label mb-2">Variables a agrupar</p>
          <div className="flex flex-wrap gap-2">
            {rankableVariables.map((variable) => (
              <button
                key={variable.id}
                type="button"
                onClick={() => toggle(variable.id)}
                className={`colmena-badge cursor-pointer ${
                  variableIds.includes(variable.id) ? 'bg-amber text-white' : 'bg-amber/10 text-yellowDark'
                }`}
              >
                {variable.code}
              </button>
            ))}
          </div>
        </div>
      ) : (
        <p className="mt-3 text-xs text-muted">Este proyecto no tiene variables ordinales o de escala para segmentar.</p>
      )}

      <div className="mt-3 flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <span className="colmena-label">Segmentos (k)</span>
          <div className="flex rounded-lg bg-surfaceSoft p-0.5">
            {K_OPTIONS.map((option) => (
              <button
                key={option}
                type="button"
                className={`colmena-pill-tab ${k === option ? 'active' : ''}`}
                onClick={() => setK(option)}
              >
                {option}
              </button>
            ))}
          </div>
        </div>
        <Button
          disabled={variableIds.length === 0}
          loading={mutation.isPending}
          onClick={() => mutation.mutate()}
          size="sm"
          type="button"
        >
          <Layers size={14} /> Calcular segmentos
        </Button>
      </div>

      {mutation.isError ? <p className="mt-3 text-xs font-medium text-danger">{mutation.error?.message}</p> : null}

      {clusterData ? (
        <div className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-2">
          {clusterData.cluster_sizes.map((size, clusterIndex) => {
            const share = clusterData.n ? Math.round((size / clusterData.n) * 100) : 0;
            return (
              <div key={clusterIndex} className="rounded-2xl border border-border p-4">
                <div className="flex items-center justify-between gap-2">
                  <p className="text-sm font-semibold text-dark">Segmento {clusterIndex + 1}</p>
                  <span className="text-xs text-muted">n = {size} · {share}%</span>
                </div>
                <dl className="mt-3 space-y-1.5 text-xs">
                  {clusterData.variable_codes.map((code, varIndex) => {
                    const variable = rankableVariables.find((item) => item.code === code);
                    return (
                      <div key={code} className="flex items-center justify-between gap-2">
                        <dt className="truncate text-muted">{variable?.name || code}</dt>
                        <dd className="shrink-0 font-mono font-semibold text-dark">
                          {formatNumber(clusterData.centroids[clusterIndex]?.[varIndex], { decimals: 2 })}
                        </dd>
                      </div>
                    );
                  })}
                </dl>
              </div>
            );
          })}
          <p className="text-[11px] text-muted sm:col-span-2">
            Los valores por segmento son el centroide (promedio) de cada variable seleccionada. Un segmento con pocos
            casos puede acercarse a identificar personas — interprétalo con cautela.
          </p>
        </div>
      ) : (
        <div className="mt-4 rounded-xl border border-dashed border-border p-5 text-sm text-muted">
          Elige al menos una variable y calcula para ver los segmentos.
        </div>
      )}
    </Card>
  );
}

export default function ProjectPremiumDashboardPage() {
  const { projectId } = useParams();
  useActiveProject(projectId);
  const [studyId, setStudyId] = useState(null);

  const { data: project, isLoading: isLoadingProject } = useQuery({
    queryKey: ['project', projectId],
    queryFn: () => getProject(projectId),
  });
  const { data: telemetry } = useQuery({
    queryKey: ['projectTelemetry', projectId],
    queryFn: () => getProjectTelemetry(projectId),
    enabled: Boolean(projectId),
  });
  const { data: overview, isLoading: isLoadingOverview } = useQuery({
    queryKey: ['resultsOverview', studyId],
    queryFn: () => getResultsOverview(studyId),
    enabled: Boolean(studyId),
  });
  const { data: variablesData } = useQuery({
    queryKey: ['variables', projectId],
    queryFn: () => listVariables(projectId, { page: 1, pageSize: 200 }),
    enabled: Boolean(projectId),
  });

  if (isLoadingProject) return <LoadingState label="Cargando..." />;
  if (!project) return <ProjectMissingState />;

  const selectedTelemetry = (telemetry?.studies || []).find((study) => study.study_id === studyId);
  const results = overview?.results || [];
  const dimensions = results.filter((result) => result.construct_type === 'DIMENSION' && !result.suppressed);
  const subdimensions = results.filter((result) => result.construct_type === 'SUBDIMENSION' && !result.suppressed);
  const rankableVariables = (variablesData?.items || []).filter((variable) =>
    ['ORDINAL', 'SCALE'].includes(variable.measurement_level),
  );

  const byPriority = (a, b) => {
    const rankA = a.priority_rank ?? Infinity;
    const rankB = b.priority_rank ?? Infinity;
    if (rankA !== rankB) return rankA - rankB;
    return unfavorablePct(b) - unfavorablePct(a);
  };

  const priorityDimensions = dimensions.filter((result) => semanticBand(dominantBand(result)?.label) === 'unfavorable');
  const worstGap = [...dimensions].sort((a, b) => unfavorablePct(b) - unfavorablePct(a))[0];
  const priorityRows = [...dimensions].sort(byPriority);
  const subdimensionRows = [...subdimensions].sort(byPriority);

  const coveragePct = selectedTelemetry?.started_count
    ? Math.round((selectedTelemetry.valid_count / selectedTelemetry.started_count) * 100)
    : null;

  return (
    <div className="colmena-page">
      <PageHeader
        eyebrow="Tablero premium"
        title={project.name}
        description="Resumen de decisión: participación, distribución oficial por dimensión, prioridades y análisis exploratorios en una sola vista."
      />

      <Card>
        <StudySelector projectId={projectId} studyId={studyId} onStudyChange={setStudyId} />
      </Card>

      {!studyId ? (
        <Card>
          <EmptyState title="Elige una aplicación o estudio." description="El tablero se arma con la telemetría y los resultados calculados de esa aplicación." />
        </Card>
      ) : isLoadingOverview ? (
        <LoadingState label="Cargando tablero…" />
      ) : (
        <>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-5">
            <MetricCard icon={Users} label="Respuestas válidas" value={selectedTelemetry?.valid_count ?? '—'} />
            <MetricCard icon={Activity} label="Tasa de válidas" value={coveragePct === null ? '—' : `${coveragePct}%`} />
            <MetricCard
              icon={AlertTriangle}
              label="Dimensiones en nivel desfavorable"
              value={dimensions.length ? `${priorityDimensions.length} / ${dimensions.length}` : '—'}
            />
            <MetricCard
              icon={Target}
              label="Mayor brecha"
              value={worstGap ? `${formatPercent(unfavorablePct(worstGap), { decimals: 0 })}` : '—'}
            />
            <MetricCard icon={Clock} label="Duración promedio" value={formatDuration(selectedTelemetry?.avg_duration_seconds)} />
          </div>
          {worstGap ? <p className="text-xs text-muted">Mayor brecha: {worstGap.construct_name} · n = {worstGap.n_valid}</p> : null}

          <div className="grid grid-cols-1 gap-4 xl:grid-cols-[minmax(0,1.4fr)_minmax(280px,1fr)]">
            <Card>
              <p className="text-sm font-semibold text-dark">Avance de participación</p>
              <p className="mb-4 mt-1 text-xs text-muted">Sesiones iniciadas y completadas por día, de toda la aplicación.</p>
              {selectedTelemetry?.series?.length ? (
                <div className="h-64 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={selectedTelemetry.series}>
                      <defs>
                        <linearGradient id="premiumStarted" x1="0" x2="0" y1="0" y2="1">
                          <stop offset="0%" stopColor="#F5B21A" stopOpacity={0.32} />
                          <stop offset="100%" stopColor="#F5B21A" stopOpacity={0.02} />
                        </linearGradient>
                      </defs>
                      <CartesianGrid stroke="rgba(148,163,184,0.22)" strokeDasharray="3 3" />
                      <XAxis dataKey="date" tick={{ fontSize: 11 }} />
                      <YAxis allowDecimals={false} tick={{ fontSize: 11 }} />
                      <Tooltip />
                      <Area dataKey="started" name="Iniciadas" stroke="#F5B21A" fill="url(#premiumStarted)" strokeWidth={2} />
                      <Area dataKey="completed" name="Completadas" stroke="#11B7B2" fill="transparent" strokeWidth={2} />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              ) : (
                <EmptyState title="Sin evolución todavía" description="La serie aparecerá con las primeras sesiones." />
              )}
            </Card>

            <Card>
              <p className="text-sm font-semibold text-dark">Distribución oficial por dimensión</p>
              <p className="mb-1 mt-1 text-xs text-muted">Capa metodológica · favorable / intermedio / desfavorable.</p>
              {dimensions.length ? (
                <div className="mt-2 divide-y divide-border/70">
                  {dimensions.map((result) => <DimensionDistributionRow key={result.construct_id} result={result} />)}
                </div>
              ) : (
                <EmptyState title="Sin resultados aún" description="Calcula el scoring en Resultados → Baremos." />
              )}
            </Card>
          </div>

          <Card>
            <p className="text-sm font-semibold text-dark">Priorización por dimensión</p>
            <p className="mb-3 mt-1 text-xs text-muted">
              Ordenado por prioridad calculada por el backend (o por % desfavorable si aún no hay baremo). No reemplaza el juicio técnico del equipo responsable.
            </p>
            {priorityRows.length ? (
              <>
                <PriorityBarChart rows={priorityRows} />
                <div className="mt-4">
                  <PriorityTable rows={priorityRows} />
                </div>
              </>
            ) : (
              <EmptyState title="Sin dimensiones publicables" description="Calcula el scoring para ver la priorización." />
            )}
          </Card>

          {subdimensionRows.length ? (
            <Card>
              <p className="text-sm font-semibold text-dark">Priorización por subdimensión</p>
              <p className="mb-3 mt-1 text-xs text-muted">
                Vista compacta de todas las subdimensiones a la vez, en vez de un gráfico por cada una.
              </p>
              <PriorityBarChart rows={subdimensionRows} />
            </Card>
          ) : null}

          <div className="grid grid-cols-1 gap-4 xl:grid-cols-2">
            <SpearmanCard studyId={studyId} />
            <SegmentationCard studyId={studyId} rankableVariables={rankableVariables} />
          </div>
        </>
      )}
    </div>
  );
}
