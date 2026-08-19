import { useEffect, useMemo, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Link, useParams } from 'react-router-dom';
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Line,
  LineChart,
  PolarAngleAxis,
  PolarGrid,
  Radar,
  RadarChart,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import {
  AlertTriangle,
  ArrowRight,
  BrainCircuit,
  CheckCircle2,
  CircleHelp,
  FlaskConical,
  GitCompareArrows,
  Network,
  Orbit,
  ShieldAlert,
  ShieldCheck,
  Sigma,
  Sparkles,
  Target,
  TrendingUp,
  Users,
} from 'lucide-react';

import { getIntelligenceSummary } from '../../../api/analytics.js';
import { getProject } from '../../../api/projects.js';
import { listStudies } from '../../../api/studies.js';
import { useActiveProject } from '../../../hooks/useActiveProject.js';
import StudySelector from '../../../components/colmena/StudySelector.jsx';
import { Button } from '../../../components/ui/Button.jsx';
import { Card } from '../../../components/ui/Card.jsx';
import { EmptyState } from '../../../components/ui/EmptyState.jsx';
import { ErrorState } from '../../../components/ui/ErrorState.jsx';
import { LoadingState } from '../../../components/ui/LoadingState.jsx';
import { ProjectMissingState } from '../../../components/colmena/ProjectMissingState.jsx';

const COLORS = { teal: '#18a7a1', amber: '#d59b27', red: '#e25b5b', green: '#18a77f', ink: '#16383d', violet: '#7c6ecf' };

function number(value, digits = 2) {
  return value === null || value === undefined ? '?' : Number(value).toFixed(digits);
}

function Metric({ icon: Icon, label, value, detail, status = 'neutral' }) {
  const tone = status === 'good' ? 'bg-emerald-50 text-emerald-700' : status === 'warning' ? 'bg-amber/15 text-yellowDark' : status === 'danger' ? 'bg-red-50 text-danger' : 'bg-[#16383d] text-white';
  return <div className="rounded-2xl border border-white/70 bg-white/84 p-4 shadow-[0_14px_36px_rgba(22,56,61,.07)] backdrop-blur-xl"><div className="flex items-start justify-between"><span className={`flex h-9 w-9 items-center justify-center rounded-xl ${tone}`}><Icon size={17} /></span><span className={`rounded-full px-2 py-1 text-[8px] font-black uppercase tracking-wider ${tone}`}>{status === 'good' ? 'Sólido' : status === 'warning' ? 'Revisar' : status === 'danger' ? 'Alerta' : 'Dato'}</span></div><p className="mt-4 text-[9px] font-black uppercase tracking-[.12em] text-muted">{label}</p><p className="mt-1 text-2xl font-black tracking-tight text-dark">{value}</p><p className="mt-1 text-[10px] leading-4 text-muted">{detail}</p></div>;
}

function Heading({ kicker, title, description, action }) {
  return <div className="mb-5 flex flex-wrap items-start justify-between gap-3"><div><p className="text-[9px] font-black uppercase tracking-[.16em] text-turquoise">{kicker}</p><h2 className="mt-1 text-lg font-black tracking-tight text-dark">{title}</h2><p className="mt-1 max-w-3xl text-xs leading-5 text-muted">{description}</p></div>{action}</div>;
}

function ReliabilityBadge({ value }) {
  const tone = value >= .8 ? 'bg-emerald-50 text-emerald-700' : value >= .7 ? 'bg-amber/15 text-yellowDark' : 'bg-red-50 text-danger';
  return <span className={`rounded-full px-2 py-1 font-mono text-[10px] font-black ${tone}`}>{number(value, 3)}</span>;
}

function CorrelationHeatmap({ dimensions, correlations }) {
  const codes = dimensions.map((item) => item.code);
  const map = new Map();
  correlations.forEach((item) => { map.set(`${item.x}|${item.y}`, item); map.set(`${item.y}|${item.x}`, item); });
  const cell = (x, y) => x === y ? { rho: 1, significant: true } : map.get(`${x}|${y}`);
  return <div className="overflow-x-auto"><table className="min-w-[620px] w-full border-separate border-spacing-1 text-center text-[10px]"><thead><tr><th className="p-2 text-left text-muted">ρ Spearman</th>{codes.map((code) => <th key={code} className="p-2 font-black text-dark">{code}</th>)}</tr></thead><tbody>{codes.map((row) => <tr key={row}><th className="p-2 text-left font-black text-dark">{row}</th>{codes.map((column) => { const value = cell(row, column); const rho = value?.rho; const magnitude = Math.abs(rho || 0); const background = rho === undefined ? '#f5f7f8' : rho >= 0 ? `rgba(24,167,161,${.12 + magnitude * .68})` : `rgba(226,91,91,${.12 + magnitude * .68})`; return <td key={column} title={value ? `${row} ↔ ${column}: ρ=${number(rho, 3)}${value.significant ? ' · significativo ajustado' : ''}` : 'Sin dato'} className={`h-11 min-w-11 rounded-lg font-mono font-black ${magnitude > .55 ? 'text-white' : 'text-dark'}`} style={{ background }}>{rho === undefined ? '—' : number(rho, 2)}{value?.significant && row !== column ? <span className="ml-0.5 align-super text-[7px]">*</span> : null}</td>; })}</tr>)}</tbody></table><div className="mt-3 flex flex-wrap items-center gap-3 text-[10px] text-muted"><span className="h-3 w-3 rounded bg-turquoise/60" /> Asociación positiva <span className="h-3 w-3 rounded bg-danger/60" /> Asociación negativa <span className="font-black text-dark">*</span> q ajustado &lt; .05</div></div>;
}

export default function ProjectAnalyticsLabPage() {
  const { projectId } = useParams();
  useActiveProject(projectId);
  const [studyId, setStudyId] = useState(null);
  const projectQuery = useQuery({ queryKey: ['project', projectId], queryFn: () => getProject(projectId) });
  const studiesQuery = useQuery({ queryKey: ['studies', projectId, 'analytics-lab'], queryFn: () => listStudies(projectId, { page: 1, pageSize: 100 }) });
  useEffect(() => { if (!studyId && studiesQuery.data?.items?.length) setStudyId(studiesQuery.data.items[0].id); }, [studyId, studiesQuery.data]);
  const summaryQuery = useQuery({ queryKey: ['intelligence-summary', studyId], queryFn: () => getIntelligenceSummary(studyId), enabled: Boolean(studyId), staleTime: 60000 });

  if (projectQuery.isLoading) return <LoadingState label="Preparando el laboratorio…" />;
  if (!projectQuery.data) return <ProjectMissingState />;
  const data = summaryQuery.data;
  const dimensions = data?.dimensions || [];
  const reliable = dimensions.filter((item) => Math.min(item.alpha || 0, item.omega || 0) >= .7).length;
  const normalityChart = dimensions.map((item) => ({ code: item.code, p: item.normality_p, delta: item.sensitivity_delta, outliers: item.outlier_count }));
  const reliabilityChart = dimensions.map((item) => ({ code: item.code, alpha: item.alpha, omega: item.omega }));
  const clusterRadar = useMemo(() => {
    if (!data?.clustering?.profiles?.length) return [];
    return dimensions.map((dimension) => ({ dimension: dimension.code, ...Object.fromEntries(data.clustering.profiles.map((profile) => [`P${profile.cluster_id}`, profile.centroids[dimension.code]])) }));
  }, [data, dimensions]);

  return (
    <div className="colmena-page pb-16">
      <section className="relative overflow-hidden rounded-[30px] border border-white/15 bg-gradient-to-br from-[#0d2d31] via-[#153e42] to-[#2f315d] p-6 text-white shadow-[0_30px_80px_rgba(16,47,51,.24)] sm:p-8">
        <div className="absolute -right-16 -top-24 h-72 w-72 rounded-full bg-violet-400/15 blur-3xl" />
        <div className="relative grid gap-6 xl:grid-cols-[1.25fr_.75fr] xl:items-end"><div><span className="inline-flex items-center gap-2 rounded-full border border-white/15 bg-white/10 px-3 py-1.5 text-[10px] font-black uppercase tracking-[.15em] text-[#cfc9ff]"><BrainCircuit size={14} /> Colmena Intelligence</span><h1 className="mt-4 text-2xl font-black tracking-tight sm:text-3xl">Laboratorio estadístico y psicométrico</h1><p className="mt-3 max-w-3xl text-sm leading-6 text-white/65">El motor evalúa supuestos, confiabilidad, robustez, asociaciones y perfiles antes de sugerir una prueba. Los resultados complementan CENSOPAS; no reemplazan su clasificación.</p><div className="mt-5 flex flex-wrap gap-2">{['Confiabilidad', 'Normalidad', 'Sensibilidad', 'Spearman + FDR', 'Clustering agregado'].map((label) => <span key={label} className="rounded-full border border-white/10 bg-white/8 px-3 py-1 text-[10px] font-bold text-white/70">{label}</span>)}</div></div><div className="rounded-2xl border border-white/15 bg-white/10 p-4 backdrop-blur-xl"><p className="text-[9px] font-black uppercase tracking-wider text-white/45">Aplicación analizada</p><div className="mt-3 [&_label]:text-white/65 [&_select]:border-white/15 [&_select]:bg-white/10 [&_select]:text-white"><StudySelector projectId={projectId} studyId={studyId} onStudyChange={setStudyId} /></div><div className="mt-4 flex items-center gap-2 text-[10px] text-white/55"><ShieldCheck size={13} className="text-[#9ce8e4]" /> Salida agregada · n mínimo {data?.min_publishable_n || 5}</div></div></div>
      </section>

      {!studyId || summaryQuery.isLoading ? <LoadingState label="Evaluando supuestos y estabilidad…" /> : summaryQuery.isError ? <ErrorState title="No se pudo construir la inteligencia estadística" message={summaryQuery.error?.message} /> : !dimensions.length ? <Card><EmptyState title="Sin puntajes dimensionales" description="Ejecuta primero el scoring CENSOPAS." /></Card> : <>
        <section className="grid gap-3 sm:grid-cols-2 xl:grid-cols-5">
          <Metric icon={Users} label="Muestra analítica" value={data.n} detail="Sesiones válidas de la última corrida" status="good" />
          <Metric icon={ShieldCheck} label="Confiabilidad" value={`${reliable}/${dimensions.length}`} detail="Dimensiones con ? y ? aceptables" status={reliable === dimensions.length ? 'good' : 'warning'} />
          <Metric icon={FlaskConical} label="No normalidad" value={`${data.quality.non_normal_dimensions}/${dimensions.length}`} detail="Decisión basada en prueba y forma" status={data.quality.non_normal_dimensions ? 'warning' : 'good'} />
          <Metric icon={ShieldAlert} label="Outliers robustos" value={data.quality.outlier_sessions} detail={`${number(data.quality.outlier_pct, 1)}% de sesiones; no se eliminan automáticamente`} status={data.quality.outlier_sessions ? 'warning' : 'good'} />
          <Metric icon={GitCompareArrows} label="Sensibilidad máxima" value={`${number(data.quality.sensitivity_max_delta, 2)} pts`} detail="Cambio al excluir atípicos solo para contraste" status={data.quality.sensitivity_max_delta > 3 ? 'danger' : 'good'} />
        </section>

        <Card>
          <Heading kicker="Motor de decisión" title="Qué prueba corresponde y por qué" description="La recomendación se deriva de la forma de las distribuciones, escala de medición, número de grupos y estabilidad; no de una selección manual arbitraria." action={<span className="rounded-full bg-violet-50 px-3 py-1 text-[9px] font-black uppercase tracking-wider text-violet-700">{data.engine}</span>} />
          <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">{[[FlaskConical, 'Distribución', data.decision.normality_summary, data.quality.non_normal_dimensions ? 'VIGILANCIA' : 'COMPATIBLE'], [GitCompareArrows, 'Comparar grupos', data.decision.recommended_comparison, 'AUTO'], [Network, 'Asociaciones', data.decision.recommended_correlation, 'ORDINAL'], [ShieldAlert, 'Casos atípicos', data.decision.outlier_policy, 'ROBUSTO']].map(([Icon, title, detail, badge]) => <div key={title} className="rounded-2xl border border-border bg-surfaceSoft/55 p-4"><div className="flex items-center justify-between"><Icon size={17} className="text-turquoise" /><span className="rounded-full bg-white px-2 py-1 text-[8px] font-black text-muted shadow-sm">{badge}</span></div><p className="mt-3 text-xs font-black text-dark">{title}</p><p className="mt-1 text-[10px] leading-4 text-muted">{detail}</p></div>)}</div>
        </Card>

        <section className="grid gap-4 xl:grid-cols-2">
          <Card>
            <Heading kicker="Psicometría" title="Confiabilidad por dimensión" description="α y ω se presentan juntos. Las líneas marcan el mínimo aceptable (.70) y el objetivo sólido (.80)." />
            <div className="h-[330px]"><ResponsiveContainer width="100%" height="100%"><BarChart data={reliabilityChart} margin={{ top: 14, right: 12, left: 0, bottom: 0 }}><CartesianGrid strokeDasharray="3 3" vertical={false} /><XAxis dataKey="code" tick={{ fontSize: 10, fontWeight: 700 }} /><YAxis domain={[0, 1]} tick={{ fontSize: 10 }} /><Tooltip formatter={(value) => number(value, 3)} /><Legend /><ReferenceLine y={.7} stroke={COLORS.amber} strokeDasharray="5 4" label={{ value: 'mín. .70', fontSize: 9, fill: COLORS.amber }} /><ReferenceLine y={.8} stroke={COLORS.green} strokeDasharray="5 4" label={{ value: 'meta .80', fontSize: 9, fill: COLORS.green }} /><Bar dataKey="alpha" name="Alfa" fill={COLORS.teal} radius={[5,5,0,0]} /><Bar dataKey="omega" name="Omega" fill={COLORS.violet} radius={[5,5,0,0]} /></BarChart></ResponsiveContainer></div>
            <div className="mt-4 overflow-x-auto rounded-2xl border border-border"><table className="min-w-[680px] w-full text-left text-[10px]"><thead className="bg-surfaceSoft"><tr>{['Dimensión', 'n', 'Ítems', 'α', 'ω', 'Lectura'].map((label) => <th key={label} className="px-3 py-2.5 font-black uppercase tracking-wider text-muted">{label}</th>)}</tr></thead><tbody>{dimensions.map((item) => <tr key={item.construct_id} className="border-t border-border"><td className="px-3 py-3"><strong className="text-dark">{item.code}</strong><span className="ml-2 text-muted">{item.name}</span></td><td className="px-3 py-3 font-mono">{item.n}</td><td className="px-3 py-3 font-mono">{item.n_items}</td><td className="px-3 py-3"><ReliabilityBadge value={item.alpha} /></td><td className="px-3 py-3"><ReliabilityBadge value={item.omega} /></td><td className="px-3 py-3 font-bold text-dark">{item.reliability_status}</td></tr>)}</tbody></table></div>
          </Card>

          <Card>
            <Heading kicker="Supuestos" title="Normalidad y análisis robusto" description="La línea roja marca p=.05. Para puntajes ordinales agregados, la forma y la robustez pesan más que una prueba aislada." />
            <div className="h-[300px]"><ResponsiveContainer width="100%" height="100%"><LineChart data={normalityChart} margin={{ top: 12, right: 18, left: 0, bottom: 0 }}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="code" tick={{ fontSize: 10, fontWeight: 700 }} /><YAxis domain={[0, 'auto']} tick={{ fontSize: 10 }} /><Tooltip formatter={(value, name) => [number(value, name === 'p' ? 4 : 2), name === 'p' ? 'p normalidad' : '? sensibilidad']} /><ReferenceLine y={.05} stroke={COLORS.red} strokeDasharray="5 4" label={{ value: 'p=.05', fill: COLORS.red, fontSize: 9 }} /><Line type="monotone" dataKey="p" name="p" stroke={COLORS.violet} strokeWidth={2.5} dot={{ r: 4, fill: COLORS.violet }} /><Line type="monotone" dataKey="delta" name="Delta" stroke={COLORS.amber} strokeWidth={2} dot={{ r: 3 }} /></LineChart></ResponsiveContainer></div>
            <div className="grid gap-2 sm:grid-cols-2">{dimensions.map((item) => <div key={item.code} className="flex items-center justify-between gap-3 rounded-xl border border-border p-3"><div><p className="text-xs font-black text-dark">{item.code} ? {item.normality_status === 'NO_NORMAL' ? 'No normal' : 'Compatible'}</p><p className="mt-0.5 text-[9px] text-muted">{item.normality_test || 'Sin prueba'} ? p {number(item.normality_p, 4)} ? {item.outlier_count} atípicos</p></div><span className={`h-2.5 w-2.5 shrink-0 rounded-full ${item.normality_status === 'NO_NORMAL' ? 'bg-amber' : 'bg-emerald-500'}`} /></div>)}</div>
          </Card>
        </section>

        <Card>
          <Heading kicker="Relaciones" title="Matriz de correlaciones dimensionales" description="Spearman es coherente con datos ordinales y distribuciones no normales. El ajuste Benjamini–Hochberg controla falsos descubrimientos en comparaciones múltiples." action={<span className="rounded-full bg-turquoise/10 px-3 py-1 text-[9px] font-black text-turquoise">{data.correlations.filter((item) => item.significant).length} asociaciones ajustadas</span>} />
          <div className="grid gap-5 xl:grid-cols-[1.12fr_.88fr]"><CorrelationHeatmap dimensions={dimensions} correlations={data.correlations} /><div className="space-y-2">{data.correlations.slice(0, 8).map((item, index) => <div key={`${item.x}-${item.y}`} className="flex items-center gap-3 rounded-xl border border-border p-3"><span className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-lg font-mono text-[10px] font-black ${item.significant ? 'bg-turquoise text-white' : 'bg-slate-100 text-muted'}`}>{index + 1}</span><div className="min-w-0 flex-1"><p className="truncate text-xs font-bold text-dark">{item.x} ? {item.y}</p><p className="text-[9px] text-muted">n={item.n} ? q={number(item.adjusted_p_value, 4)} ? {item.magnitude}</p></div><strong className="font-mono text-sm text-dark">? {number(item.rho, 2)}</strong></div>)}</div></div>
        </Card>

        <section className="grid gap-4 xl:grid-cols-[1.05fr_.95fr]">
          <Card>
            <Heading kicker="Patrones ocultos" title="Perfiles agregados de exposición" description="K-means exploratorio sobre dimensiones escaladas robustamente. Se publican tamaños y centroides; nunca la asignación de una persona." action={<span className={`rounded-full px-3 py-1 text-[9px] font-black ${data.clustering.status === 'AVAILABLE' ? 'bg-emerald-50 text-emerald-700' : 'bg-slate-100 text-muted'}`}>{data.clustering.status}</span>} />
            {data.clustering.status === 'AVAILABLE' ? <><div className="h-[360px]"><ResponsiveContainer width="100%" height="100%"><RadarChart data={clusterRadar}><PolarGrid stroke="#d6dde0" /><PolarAngleAxis dataKey="dimension" tick={{ fontSize: 10, fontWeight: 800 }} />{data.clustering.profiles.map((profile, index) => <Radar key={profile.cluster_id} name={profile.label} dataKey={`P${profile.cluster_id}`} stroke={[COLORS.red, COLORS.amber, COLORS.teal][index]} fill={[COLORS.red, COLORS.amber, COLORS.teal][index]} fillOpacity={.12} strokeWidth={2} />)}<Legend /><Tooltip /></RadarChart></ResponsiveContainer></div><div className="grid gap-2 sm:grid-cols-3">{data.clustering.profiles.map((profile, index) => <div key={profile.cluster_id} className="rounded-xl border border-border p-3"><div className="flex items-center justify-between"><span className="h-2.5 w-2.5 rounded-full" style={{ background: [COLORS.red, COLORS.amber, COLORS.teal][index] }} /><strong className="font-mono text-sm text-dark">n={profile.n}</strong></div><p className="mt-2 text-xs font-black text-dark">{profile.label}</p><p className="mt-1 text-[9px] text-muted">Índice {number(profile.risk_index, 1)} · perfil {profile.cluster_id}</p></div>)}</div><p className="mt-3 text-[10px] text-muted">Silhouette: <strong className="text-dark">{number(data.clustering.silhouette, 3)}</strong>. Se interpreta como exploratorio; estabilidad limitada si el valor es bajo.</p></> : <EmptyState title="Clustering no disponible" description={data.clustering.reason} />}
          </Card>

          <Card>
            <Heading kicker="Sensibilidad" title="¿Cambian las decisiones sin atípicos?" description="El resultado principal conserva todos los casos válidos. Esta vista mide cuánto se movería la media en un escenario de sensibilidad." />
            <div className="space-y-3">{dimensions.map((item) => { const critical = item.sensitivity_delta >= 3; const moderate = item.sensitivity_delta >= 1; return <div key={item.code} className="rounded-2xl border border-border p-4"><div className="flex items-start justify-between gap-3"><div><p className="text-xs font-black text-dark">{item.code} ? {item.name}</p><p className="mt-1 text-[9px] text-muted">Media {number(item.mean)} ? robusta {number(item.sensitivity_mean)} ? IC mediana [{number(item.median_ci_lower)}, {number(item.median_ci_upper)}]</p></div><span className={`rounded-full px-2 py-1 text-[9px] font-black ${critical ? 'bg-red-50 text-danger' : moderate ? 'bg-amber/15 text-yellowDark' : 'bg-emerald-50 text-emerald-700'}`}>? {number(item.sensitivity_delta)}</span></div><div className="mt-3 h-1.5 overflow-hidden rounded-full bg-slate-100"><div className={`h-full rounded-full ${critical ? 'bg-danger' : moderate ? 'bg-amber' : 'bg-emerald-500'}`} style={{ width: `${Math.min(100, item.sensitivity_delta * 20)}%` }} /></div></div>; })}</div>
          </Card>
        </section>

        <Card className="border-amber/25 bg-gradient-to-br from-amber/6 to-white">
          <div className="flex items-start gap-3"><CircleHelp className="mt-0.5 shrink-0 text-amber" size={20} /><div><p className="text-sm font-black text-dark">Límites de interpretación</p><div className="mt-2 grid gap-2 md:grid-cols-2">{data.limitations.map((item) => <p key={item} className="flex items-start gap-2 text-[10px] leading-4 text-muted"><span className="mt-1 h-1.5 w-1.5 shrink-0 rounded-full bg-amber" />{item}</p>)}</div><Link to={`/colmena/project/${projectId}/reports`}><Button className="mt-4" size="sm">Incorporar al expediente <ArrowRight size={14} /></Button></Link></div></div>
        </Card>
      </>}
    </div>
  );
}
