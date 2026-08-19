import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Link, useParams } from 'react-router-dom';
import {
  Activity,
  ArrowRight,
  BarChart3,
  CheckCircle2,
  ClipboardCheck,
  Clock3,
  Copy,
  ExternalLink,
  FileCheck2,
  Gauge,
  Link2,
  ListChecks,
  LockKeyhole,
  Radar,
  RefreshCcw,
  ShieldCheck,
  Target,
  Users,
} from 'lucide-react';

import { getDemoCampaign } from '../../../api/demo.js';
import { getProject } from '../../../api/projects.js';
import { getProjectTelemetry } from '../../../api/telemetry.js';
import { useActiveProject } from '../../../hooks/useActiveProject.js';
import { Button } from '../../../components/ui/Button.jsx';
import { Card } from '../../../components/ui/Card.jsx';
import { ErrorState } from '../../../components/ui/ErrorState.jsx';
import { LoadingState } from '../../../components/ui/LoadingState.jsx';
import { ProjectMissingState } from '../../../components/colmena/ProjectMissingState.jsx';

function ProgressRing({ value, label }) {
  const safe = Math.max(0, Math.min(100, Number(value || 0)));
  return <div className="relative flex h-24 w-24 items-center justify-center rounded-full" style={{ background: `conic-gradient(#4fd1c5 ${safe * 3.6}deg, rgba(255,255,255,.12) 0deg)` }}><div className="flex h-[76px] w-[76px] flex-col items-center justify-center rounded-full bg-[#153b3f]"><strong className="text-xl font-black text-white">{Math.round(safe)}%</strong><span className="text-[9px] uppercase tracking-wider text-white/45">{label}</span></div></div>;
}

function Phase({ number, title, detail, state, to }) {
  const complete = state === 'complete';
  const active = state === 'active';
  const body = <div className={`group flex h-full items-start gap-3 rounded-2xl border p-4 transition ${active ? 'border-amber/45 bg-amber/7 shadow-[0_12px_30px_rgba(213,155,39,.08)]' : complete ? 'border-turquoise/25 bg-turquoise/5' : 'border-border bg-white'}`}><span className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-xl text-xs font-black ${complete ? 'bg-turquoise text-white' : active ? 'bg-amber text-dark' : 'bg-slate-100 text-muted'}`}>{complete ? <CheckCircle2 size={15} /> : number}</span><div><p className="text-xs font-black text-dark">{title}</p><p className="mt-1 text-[10px] leading-4 text-muted">{detail}</p>{active ? <span className="mt-2 inline-flex items-center gap-1 text-[10px] font-bold text-yellowDark">Continuar <ArrowRight size={11} /></span> : null}</div></div>;
  return to ? <Link to={to}>{body}</Link> : body;
}

function Threshold({ label, value, target, critical, direction = 'higher' }) {
  const current = Number(value || 0);
  const ok = direction === 'higher' ? current >= target : current < target;
  const danger = direction === 'higher' ? current < critical : current >= critical;
  const tone = danger ? { bar: '#e25b5b', bg: 'bg-red-50', text: 'text-danger', status: 'Crítico' } : ok ? { bar: '#18a77f', bg: 'bg-emerald-50', text: 'text-emerald-700', status: 'Meta' } : { bar: '#d59b27', bg: 'bg-amber/12', text: 'text-yellowDark', status: 'Vigilancia' };
  return <div className="rounded-2xl border border-border bg-white p-4"><div className="flex items-start justify-between gap-3"><div><p className="text-[10px] font-extrabold uppercase tracking-wider text-muted">{label}</p><p className="mt-1 text-xl font-black text-dark">{current.toFixed(1)}%</p></div><span className={`rounded-full px-2.5 py-1 text-[9px] font-extrabold ${tone.bg} ${tone.text}`}>{tone.status}</span></div><div className="relative mt-4 h-2 rounded-full bg-slate-100"><div className="h-full rounded-full transition-all" style={{ width: `${Math.min(current, 100)}%`, backgroundColor: tone.bar }} /><span className="absolute -top-1 h-4 w-0.5 bg-dark/45" style={{ left: `${Math.min(target, 100)}%` }} /></div><div className="mt-2 flex justify-between text-[9px] font-semibold text-muted"><span>0%</span><span>Meta {target}%</span><span>100%</span></div></div>;
}

export default function CampaignOverviewPage() {
  const { projectId } = useParams();
  useActiveProject(projectId);
  const [copied, setCopied] = useState(false);
  const projectQuery = useQuery({ queryKey: ['project', projectId], queryFn: () => getProject(projectId) });
  const project = projectQuery.data;
  const hasCampaign = Boolean(project?.metadata?.demo_campaign);
  const demoQuery = useQuery({ queryKey: ['demo-campaign', projectId], queryFn: () => getDemoCampaign(projectId), enabled: hasCampaign });
  const telemetryQuery = useQuery({ queryKey: ['projectTelemetry', projectId], queryFn: () => getProjectTelemetry(projectId), enabled: hasCampaign, refetchInterval: 15000 });

  if (projectQuery.isLoading) return <LoadingState label="Abriendo la campaña…" />;
  if (projectQuery.isError) return <ErrorState title="No pudimos abrir la campaña" message={projectQuery.error?.message} />;
  if (!project) return <ProjectMissingState />;

  const metadata = project.metadata || {};
  const thresholds = { coverage_target: 85, coverage_critical: 65, completion_target: 90, risk_warning: 35, risk_critical: 50, ...(metadata.thresholds || {}) };
  const telemetry = telemetryQuery.data?.studies?.[0];
  const expected = Number(metadata.expected_worker_count || 0);
  const valid = Number(telemetry?.valid_count || demoQuery.data?.synthetic_responses || 0);
  const started = Number(telemetry?.started_count || valid);
  const completed = Number(telemetry?.completed_count || valid);
  const coverage = expected ? valid / expected * 100 : 0;
  const completion = started ? completed / started * 100 : 0;
  const publicPath = demoQuery.data?.public_path;
  const publicUrl = publicPath ? `${window.location.origin}${publicPath}` : null;
  const versionLabel = metadata.instrument_version_kind === 'SHORT' ? 'Versión corta' : 'Versión media';

  const copy = async () => {
    if (!publicUrl) return;
    await navigator.clipboard.writeText(publicUrl);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1800);
  };

  return (
    <div className="colmena-page pb-16">
      <section className="relative overflow-hidden rounded-[30px] border border-white/15 bg-gradient-to-br from-[#0d2d31] via-[#153e42] to-[#17635f] p-6 text-white shadow-[0_30px_80px_rgba(16,47,51,.24)] sm:p-8">
        <div className="absolute right-0 top-0 h-64 w-64 rounded-full bg-turquoise/15 blur-3xl" />
        <div className="relative grid gap-7 xl:grid-cols-[1.25fr_.75fr] xl:items-center">
          <div><div className="flex flex-wrap items-center gap-2"><span className="rounded-full border border-white/15 bg-white/10 px-3 py-1.5 text-[10px] font-extrabold uppercase tracking-[.14em] text-[#9ce8e4]">Campaña empresarial</span><span className="inline-flex items-center gap-1.5 rounded-full bg-emerald-400/15 px-3 py-1.5 text-[10px] font-extrabold text-emerald-200"><span className="h-1.5 w-1.5 animate-pulse rounded-full bg-emerald-300" /> En campo</span></div><h1 className="mt-4 text-2xl font-black tracking-tight sm:text-3xl">{project.name}</h1><p className="mt-2 text-sm text-white/65">{versionLabel} · {expected || '—'} convocados · datos sintéticos · privacidad n ≥ {metadata.min_publishable_n || 5}</p><div className="mt-5 flex flex-wrap gap-2"><Link to={`/colmena/project/${projectId}/telemetry`}><Button className="bg-amber text-dark hover:bg-[#f6c354]"><Activity size={15} /> Ver telemetría</Button></Link><Link to={`/colmena/project/${projectId}/results`}><Button variant="ghost" className="border border-white/15 bg-white/10 text-white hover:bg-white/20"><Radar size={15} /> Abrir analítica</Button></Link><Link to={`/colmena/project/${projectId}/reports`}><Button variant="ghost" className="border border-white/15 bg-white/10 text-white hover:bg-white/20"><FileCheck2 size={15} /> Expediente</Button></Link></div></div>
          <div className="flex items-center justify-center gap-5 rounded-2xl border border-white/15 bg-white/10 p-5 backdrop-blur-xl"><ProgressRing value={coverage} label="cobertura" /><div className="min-w-0"><p className="text-[10px] font-extrabold uppercase tracking-wider text-white/45">Estado de captura</p><p className="mt-1 text-xl font-black">{valid} válidas</p><p className="mt-1 text-xs text-white/55">de {expected || '—'} trabajadores esperados</p><div className="mt-3 flex items-center gap-2 text-[10px] font-bold text-[#9ce8e4]"><ShieldCheck size={13} /> Sin respuestas individuales</div></div></div>
        </div>
      </section>

      <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
        <Phase number="1" title="Empresa y alcance" detail="Razón social, sedes, población y responsables." state="complete" to="/colmena/company" />
        <Phase number="2" title="Instrumento protegido" detail={`${versionLabel}; estructura congelada para captura.`} state="complete" to={`/colmena/project/${projectId}/form`} />
        <Phase number="3" title="Aplicación anónima" detail="Enlace activo, seguimiento y control de calidad." state="active" to={`/colmena/project/${projectId}/telemetry`} />
        <Phase number="4" title="Analítica y expediente" detail="Hallazgos, intervención, anexos y firmas." state={valid ? 'active' : 'pending'} to={`/colmena/project/${projectId}/results`} />
      </section>

      <section className="grid gap-4 xl:grid-cols-[1.08fr_.92fr]">
        <Card>
          <div className="flex flex-wrap items-start justify-between gap-3"><div><p className="text-[10px] font-extrabold uppercase tracking-[.14em] text-turquoise">Acceso de trabajadores</p><h2 className="mt-1 text-lg font-black text-dark">Enlace anónimo de la evaluación</h2><p className="mt-1 text-xs text-muted">El trabajador no necesita iniciar sesión ni entregar datos identificatorios.</p></div><span className="rounded-full bg-emerald-50 px-3 py-1 text-[10px] font-extrabold text-emerald-700">ACTIVO</span></div>
          <div className="mt-5 flex min-w-0 items-center gap-3 rounded-2xl border border-border bg-surfaceSoft p-3"><span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-white text-turquoise shadow-sm"><Link2 size={18} /></span><code className="min-w-0 flex-1 truncate text-xs font-bold text-dark">{publicUrl || 'Preparando enlace público…'}</code><Button size="sm" variant="secondary" onClick={copy} disabled={!publicUrl}><Copy size={14} /> {copied ? 'Copiado' : 'Copiar'}</Button>{publicPath ? <a href={publicPath} target="_blank" rel="noreferrer"><Button size="sm"><ExternalLink size={14} /></Button></a> : null}</div>
          <div className="mt-4 grid gap-2 sm:grid-cols-3">{[[LockKeyhole, 'Separación', 'Código y respuesta no se vinculan'], [ShieldCheck, 'Supresión', `Resultados ocultos con n < ${metadata.min_publishable_n || 5}`], [RefreshCcw, 'Actualización', 'Telemetría cada 15 segundos']].map(([Icon, title, detail]) => <div key={title} className="rounded-xl border border-border p-3"><Icon size={15} className="text-turquoise" /><p className="mt-2 text-xs font-bold text-dark">{title}</p><p className="mt-1 text-[10px] leading-4 text-muted">{detail}</p></div>)}</div>
        </Card>

        <Card>
          <div className="flex items-start justify-between gap-3"><div><p className="text-[10px] font-extrabold uppercase tracking-[.14em] text-amber">Control operacional</p><h2 className="mt-1 text-lg font-black text-dark">Embudo de participación</h2></div><Gauge size={22} className="text-amber" /></div>
          <div className="mt-5 space-y-3">{[[expected, 'Convocados', '#16383d'], [started, 'Iniciaron', '#d59b27'], [completed, 'Completaron', '#2b9c96'], [valid, 'Válidas', '#18a77f']].map(([value, label, color], index) => <div key={label}><div className="mb-1 flex items-center justify-between text-xs"><span className="font-bold text-dark">{label}</span><span className="font-mono font-black text-dark">{value}</span></div><div className="h-2.5 overflow-hidden rounded-full bg-slate-100"><div className="h-full rounded-full" style={{ width: `${expected ? Math.min(100, Number(value || 0) / expected * 100) : 0}%`, backgroundColor: color, opacity: 1 - index * .04 }} /></div></div>)}</div>
          <div className="mt-5 grid grid-cols-3 gap-2 text-center"><div className="rounded-xl bg-surfaceSoft p-3"><Clock3 size={14} className="mx-auto text-muted" /><p className="mt-1 text-sm font-black text-dark">{telemetry?.avg_duration_seconds ? `${Math.round(telemetry.avg_duration_seconds / 60)}m` : '—'}</p><p className="text-[9px] text-muted">tiempo medio</p></div><div className="rounded-xl bg-surfaceSoft p-3"><ListChecks size={14} className="mx-auto text-muted" /><p className="mt-1 text-sm font-black text-dark">{telemetry?.excluded_count || 0}</p><p className="text-[9px] text-muted">excluidas</p></div><div className="rounded-xl bg-surfaceSoft p-3"><Users size={14} className="mx-auto text-muted" /><p className="mt-1 text-sm font-black text-dark">{completion.toFixed(0)}%</p><p className="text-[9px] text-muted">completitud</p></div></div>
        </Card>
      </section>

      <section>
        <div className="mb-4 flex items-end justify-between"><div><p className="text-[10px] font-extrabold uppercase tracking-[.14em] text-turquoise">Límites de decisión</p><h2 className="mt-1 text-lg font-black text-dark">Metas, vigilancia y criticidad</h2><p className="mt-1 text-xs text-muted">La marca vertical representa la meta configurada; el color siempre está acompañado por estado textual.</p></div></div>
        <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-4"><Threshold label="Cobertura válida" value={coverage} target={thresholds.coverage_target} critical={thresholds.coverage_critical} /><Threshold label="Completitud" value={completion} target={thresholds.completion_target} critical={75} /><Threshold label="Celdas protegidas" value={100} target={100} critical={95} /><Threshold label="Trazabilidad" value={100} target={100} critical={95} /></div>
      </section>

      <section className="grid gap-3 md:grid-cols-3">
        {[[Activity, 'Telemetría', 'Participación, calidad, embudo, tiempos y cobertura.', `/colmena/project/${projectId}/telemetry`, 'Operación'], [BarChart3, 'Dashboard analítico', 'Dimensiones, subdimensiones, Áreas, confiabilidad y patrones.', `/colmena/project/${projectId}/results`, 'Decisión'], [FileCheck2, 'Expediente técnico', 'Informe estructurado, anexos, plan y cuatro firmas.', `/colmena/project/${projectId}/reports`, 'Evidencia']].map(([Icon, title, detail, to, tag]) => <Link key={title} to={to} className="group"><Card className="h-full transition group-hover:-translate-y-1 group-hover:border-turquoise/30 group-hover:shadow-lg"><div className="flex items-start justify-between"><span className="flex h-11 w-11 items-center justify-center rounded-2xl bg-[#16383d] text-white"><Icon size={19} /></span><span className="rounded-full bg-surfaceSoft px-2.5 py-1 text-[9px] font-extrabold uppercase tracking-wider text-muted">{tag}</span></div><h3 className="mt-5 text-base font-black text-dark">{title}</h3><p className="mt-2 text-xs leading-5 text-muted">{detail}</p><span className="mt-4 inline-flex items-center gap-1 text-xs font-bold text-turquoise">Abrir módulo <ArrowRight size={13} className="transition group-hover:translate-x-1" /></span></Card></Link>)}
      </section>
    </div>
  );
}
