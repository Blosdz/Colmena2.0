import { useMemo, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import { Area, AreaChart, Bar, BarChart, CartesianGrid, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { Activity, ArrowRight, CheckCircle2, CircleAlert, ClipboardCheck, Copy, ExternalLink, FileText, Link2, Play, ShieldCheck, Users } from 'lucide-react';

import { useAuth } from '../../auth/AuthContext.jsx';
import { createProject } from '../../api/projects.js';
import { createDemoCampaign } from '../../api/demo.js';
import { Card } from '../../components/ui/Card.jsx';
import MetricCard from '../../components/ui/MetricCard.jsx';
import { Button } from '../../components/ui/Button.jsx';
import { PageHeader } from '../../components/layout/PageHeader.jsx';

const DIMENSIONS = [
  { name: 'Exigencias psicológicas', unfavorable: 46, intermediate: 31, favorable: 23 },
  { name: 'Conflicto trabajo-familia', unfavorable: 29, intermediate: 36, favorable: 35 },
  { name: 'Control sobre el trabajo', unfavorable: 18, intermediate: 34, favorable: 48 },
  { name: 'Apoyo y liderazgo', unfavorable: 37, intermediate: 35, favorable: 28 },
  { name: 'Compensaciones', unfavorable: 42, intermediate: 33, favorable: 25 },
  { name: 'Capital social', unfavorable: 22, intermediate: 31, favorable: 47 },
];

const COLORS = { unfavorable: '#E05959', intermediate: '#F2B84B', favorable: '#24A886' };

function simulatedSeries(completed) {
  const checkpoints = [0, 15, 30, 45, 60, 75, 90, 100];
  return checkpoints.map((value, index) => ({
    label: `T${index + 1}`,
    iniciadas: Math.min(64, Math.round(value * 0.64)),
    válidas: Math.min(completed, Math.round(value * completed / 100)),
  }));
}

export default function DemoCampaignPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [responses, setResponses] = useState(48);
  const [version, setVersion] = useState('MEDIUM');
  const [running, setRunning] = useState(false);
  const [demo, setDemo] = useState(null);
  const valid = Math.max(0, responses - Math.round(responses * 0.035));
  const completion = Math.round((valid / 64) * 100);
  const series = useMemo(() => simulatedSeries(completion), [completion]);

  const campaignMutation = useMutation({
    mutationFn: async () => {
      const project = await createProject({
        ownerUserId: user.id,
        name: `Operación minera Andina · demo ${version === 'MEDIUM' ? 'media' : 'corta'}`,
        projectType: 'CENSO',
        description: 'Escenario sintético para demostración de campaña psicosocial anónima.',
        metadata: {
          product_mode: 'PSYCHOSOCIAL',
          methodology: 'CENSOPAS_COPSOQ',
          methodology_mode: 'COLMENA_EXPLORATORY_SYNTHETIC',
          official_equivalence_enabled: false,
          expected_worker_count: 64,
          anonymity_mode: 'ANONYMOUS_LINK',
          min_publishable_n: 5,
        },
      });
      const created = await createDemoCampaign(project.id, { version_kind: version, synthetic_responses: 48, industry: 'MINERIA' });
      return { project, created };
    },
    onSuccess: ({ project, created }) => setDemo({ ...created, projectId: project.id }),
  });

  const simulate = () => {
    setRunning(true);
    window.setTimeout(() => {
      setResponses((current) => Math.min(64, current + 8));
      setRunning(false);
    }, 450);
  };

  const publicUrl = demo ? `${window.location.origin}${demo.public_path}` : null;
  const copyLink = async () => {
    if (publicUrl && navigator.clipboard) await navigator.clipboard.writeText(publicUrl);
  };

  return (
    <div className="colmena-page">
      <PageHeader
        eyebrow="Demo sintético conectado"
        title="Operación minera Andina"
        description="Crea una campaña persistente con enlace anónimo real, 48 sesiones sintéticas y resultados exploratorios agregados."
        actions={<Link to="/colmena/project/new"><Button size="sm" variant="secondary"><ClipboardCheck size={15} /> Crear campaña de empresa</Button></Link>}
      />

      <div className="overflow-hidden rounded-3xl border border-white/30 bg-gradient-to-br from-dark via-[#1c2b33] to-[#204d4c] p-5 text-white shadow-soft sm:p-7">
        <div className="grid gap-6 lg:grid-cols-[1.35fr_0.65fr] lg:items-center">
          <div>
            <span className="inline-flex items-center gap-2 rounded-full border border-white/20 bg-white/10 px-3 py-1 text-[11px] font-bold uppercase tracking-[0.12em] text-[#9CE8E4]">
              <span className="h-1.5 w-1.5 rounded-full bg-turquoise animate-pulse" /> Escenario demo protegido
            </span>
            <h2 className="mt-4 max-w-xl text-2xl font-extrabold tracking-tight sm:text-3xl">CENSOPAS-COPSOQ con captura anónima y lectura preventiva trazable.</h2>
            <p className="mt-3 max-w-2xl text-sm leading-6 text-white/70">Las respuestas, clasificaciones y umbrales son sintéticos. El piloto nunca se presenta como evaluación oficial ni como expediente para SUNAFIL.</p>
            <div className="mt-5 flex flex-wrap gap-2">
              <span className="rounded-xl bg-white/10 px-3 py-2 text-xs font-semibold">{version === 'MEDIUM' ? 'Versión media · 112 ítems' : 'Versión corta · 42 ítems'}</span>
              <span className="rounded-xl bg-white/10 px-3 py-2 text-xs font-semibold">Link anónimo real</span>
              <span className="rounded-xl bg-white/10 px-3 py-2 text-xs font-semibold">Supresión n ≥ 5</span>
            </div>
          </div>
          <div className="rounded-2xl border border-white/15 bg-white/10 p-4 backdrop-blur-xl">
            <p className="text-[11px] font-bold uppercase tracking-[0.12em] text-white/55">Enlace de participantes</p>
            <div className="mt-2 flex items-center gap-2 rounded-xl bg-black/20 p-3 text-sm font-medium">
              <Link2 size={16} className="shrink-0 text-amber" /> {demo ? demo.public_path : 'Se genera al crear el escenario'}
            </div>
            {demo ? (
              <div className="mt-3 flex flex-wrap gap-2">
                <a href={demo.public_path} target="_blank" rel="noreferrer"><Button size="sm" variant="secondary"><ExternalLink size={14} /> Abrir encuesta</Button></a>
                <Button size="sm" variant="ghost" className="bg-white/10 text-white hover:bg-white/20" onClick={copyLink}><Copy size={14} /> Copiar</Button>
              </div>
            ) : (
              <Button className="mt-3 bg-amber text-dark hover:bg-amber/90" size="sm" onClick={() => campaignMutation.mutate()} loading={campaignMutation.isPending}>
                <Play size={14} /> Generar demo persistente
              </Button>
            )}
            {campaignMutation.isError ? <p className="mt-3 text-xs text-[#FFC5C5]">No se pudo crear la campaña. Verifica que el backend esté activo y vuelve a intentarlo.</p> : null}
          </div>
        </div>
      </div>

      {demo ? (
        <Card className="border-turquoise/30 bg-turquoise/5">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div><p className="text-sm font-bold text-dark">Demo persistente lista</p><p className="mt-1 text-xs text-muted">Instrumento, estudio abierto, sesiones sintéticas, reglas exploratorias y resultados agregados se crearon en el mismo motor.</p></div>
            <div className="flex flex-wrap gap-2">
              <Button size="sm" variant="secondary" onClick={() => navigate(`/colmena/project/${demo.projectId}/telemetry`)}>Telemetría</Button>
              <Button size="sm" variant="secondary" onClick={() => navigate(`/colmena/project/${demo.projectId}/results`)}>Resultados</Button>
              <Button size="sm" onClick={() => navigate(`/colmena/project/${demo.projectId}/reports`)}><FileText size={14} /> Reporte</Button>
            </div>
          </div>
        </Card>
      ) : null}

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <MetricCard icon={Users} label="Sesiones válidas" value={demo ? demo.synthetic_responses : valid} />
        <MetricCard icon={Activity} label="Cobertura demo" value={`${demo ? 75 : completion}%`} />
        <MetricCard icon={ShieldCheck} label="Privacidad mínima" value="n ≥ 5" />
        <MetricCard icon={CircleAlert} label="Prioridades demo" value="2" />
      </div>

      <div className="grid gap-4 xl:grid-cols-[1.2fr_0.8fr]">
        <Card>
          <div className="flex flex-wrap items-start justify-between gap-3">
            <div><p className="text-sm font-bold text-dark">Telemetría de campaña</p><p className="mt-1 text-xs text-muted">Vista de demostración de sesiones iniciadas y válidas; el proyecto creado entrega además su telemetría real.</p></div>
            <Button size="sm" onClick={simulate} loading={running} disabled={responses >= 64}><Play size={14} /> Simular 8 sesiones</Button>
          </div>
          <div className="mt-4 h-64"><ResponsiveContainer width="100%" height="100%"><AreaChart data={series}><defs><linearGradient id="validGradient" x1="0" x2="0" y1="0" y2="1"><stop offset="0%" stopColor="#11B7B2" stopOpacity={0.4} /><stop offset="100%" stopColor="#11B7B2" stopOpacity={0.02} /></linearGradient></defs><CartesianGrid stroke="rgba(148,163,184,0.18)" strokeDasharray="3 3" /><XAxis dataKey="label" tick={{ fontSize: 11 }} /><YAxis allowDecimals={false} tick={{ fontSize: 11 }} /><Tooltip /><Area type="monotone" dataKey="iniciadas" stroke="#F5B21A" fill="transparent" strokeWidth={2} /><Area type="monotone" dataKey="válidas" stroke="#11B7B2" fill="url(#validGradient)" strokeWidth={2.5} /></AreaChart></ResponsiveContainer></div>
          <div className="grid gap-2 sm:grid-cols-3"><div className="rounded-xl bg-surfaceSoft p-3"><p className="colmena-label">Incompletas</p><p className="mt-1 text-lg font-bold text-dark">2</p></div><div className="rounded-xl bg-surfaceSoft p-3"><p className="colmena-label">Atípicas</p><p className="mt-1 text-lg font-bold text-dark">1</p></div><div className="rounded-xl bg-surfaceSoft p-3"><p className="colmena-label">Tiempo medio</p><p className="mt-1 text-lg font-bold text-dark">11m</p></div></div>
        </Card>

        <Card>
          <p className="text-sm font-bold text-dark">Configuración del escenario</p>
          <p className="mt-1 text-xs leading-5 text-muted">La versión se congela al crear la campaña. Cada escenario usa el catálogo local derivado del diccionario recibido.</p>
          <div className="mt-4 grid grid-cols-2 gap-2">{['SHORT', 'MEDIUM'].map((item) => <button key={item} type="button" disabled={Boolean(demo)} onClick={() => setVersion(item)} className={`rounded-xl border p-3 text-left transition disabled:cursor-not-allowed ${version === item ? 'border-amber bg-amber/10' : 'border-border bg-surface hover:border-amber/40'}`}><p className="text-xs font-bold text-dark">{item === 'SHORT' ? 'Corta' : 'Media'}</p><p className="mt-1 text-[11px] text-muted">{item === 'SHORT' ? '42 ítems · 31 puntuables' : '112 ítems · 69 puntuables'}</p></button>)}</div>
          <div className="mt-4 space-y-2">{[['Captura', 'Anónima y voluntaria', CheckCircle2], ['Clasificación', 'Válida, incompleta o atípica', CheckCircle2], ['Privacidad', 'Supresión primaria y secundaria', ShieldCheck], ['Reporte', 'Expediente técnico preventivo', FileText]].map(([label, value, Icon]) => <div key={label} className="flex items-center gap-3 rounded-xl border border-border/70 p-3"><Icon size={17} className="text-turquoise" /><div><p className="text-xs font-bold text-dark">{label}</p><p className="text-[11px] text-muted">{value}</p></div></div>)}</div>
        </Card>
      </div>

      <Card>
        <div className="flex flex-wrap items-end justify-between gap-3"><div><p className="text-sm font-bold text-dark">Panorama preventivo agregado</p><p className="mt-1 text-xs text-muted">Distribución sintética por dimensión. La lectura operacional del proyecto se obtiene en Resultados después de crear el escenario.</p></div>{demo ? <button type="button" onClick={() => navigate(`/colmena/project/${demo.projectId}/premium`)} className="inline-flex items-center gap-1 text-sm font-semibold text-amber">Ver analítica premium <ArrowRight size={14} /></button> : null}</div>
        <div className="mt-4 h-72"><ResponsiveContainer width="100%" height="100%"><BarChart data={DIMENSIONS} layout="vertical" margin={{ left: 22 }}><CartesianGrid stroke="rgba(148,163,184,0.18)" strokeDasharray="3 3" /><XAxis type="number" domain={[0, 100]} tickFormatter={(value) => `${value}%`} /><YAxis dataKey="name" type="category" width={170} tick={{ fontSize: 11 }} /><Tooltip formatter={(value) => `${value}%`} /><Bar dataKey="favorable" stackId="risk" fill={COLORS.favorable} /><Bar dataKey="intermediate" stackId="risk" fill={COLORS.intermediate} /><Bar dataKey="unfavorable" stackId="risk" fill={COLORS.unfavorable}>{DIMENSIONS.map((row) => <Cell key={row.name} fill={COLORS.unfavorable} />)}</Bar></BarChart></ResponsiveContainer></div>
      </Card>
    </div>
  );
}