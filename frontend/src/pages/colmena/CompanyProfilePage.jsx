import { useEffect, useMemo, useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import {
  BadgeCheck,
  Building2,
  CheckCircle2,
  Contact,
  Factory,
  MapPin,
  Palette,
  Plus,
  Save,
  ShieldCheck,
  Trash2,
  Users,
} from 'lucide-react';

import { getCompanyProfile, saveCompanyProfile } from '../../api/company.js';
import { PageHeader } from '../../components/layout/PageHeader.jsx';
import { Button } from '../../components/ui/Button.jsx';
import { Card } from '../../components/ui/Card.jsx';
import { ErrorState } from '../../components/ui/ErrorState.jsx';
import { LoadingState } from '../../components/ui/LoadingState.jsx';

const SIGNATORY_ROLES = [
  'Profesional responsable',
  'Representante de la empresa',
  'Ingeniero de seguridad',
  'Psicólogo revisor',
];

const DEMO_PROFILE = {
  name: 'Andes Mineral Services',
  legal_name: 'Andes Mineral Services S.A.C.',
  tax_id: '20601234567',
  organization_type: 'EMPRESA',
  industry: 'Minería y servicios conexos',
  ciiu_code: '0710',
  fiscal_address: 'Av. República de Panamá 3545, San Isidro, Lima',
  worker_count: 250,
  representative_name: 'Mariana Salazar Ríos',
  study_lead_name: 'Diego Núñez Valdivia',
  contact_email: 'sst@andesmineral.pe',
  contact_phone: '+51 987 420 168',
  brand_color: '#D59B27',
  locations: [
    { code: 'UM-CENTRAL', name: 'Unidad Minera Central', address: 'Junín', worker_count: 150 },
    { code: 'PLANTA-SUR', name: 'Planta Sur', address: 'Arequipa', worker_count: 70 },
    { code: 'LIMA', name: 'Sede Lima', address: 'San Isidro, Lima', worker_count: 30 },
  ],
  signatories: SIGNATORY_ROLES.map((role) => ({ role, full_name: '', professional_id: '', position: '' })),
};

function normalizeProfile(profile) {
  if (!profile) return structuredClone(DEMO_PROFILE);
  const byRole = new Map((profile.signatories || []).map((item) => [item.role, item]));
  return {
    ...DEMO_PROFILE,
    ...profile,
    locations: profile.locations?.length ? profile.locations : DEMO_PROFILE.locations,
    signatories: SIGNATORY_ROLES.map((role) => ({
      role,
      full_name: '',
      professional_id: '',
      position: '',
      ...(byRole.get(role) || {}),
    })),
  };
}

function Field({ label, hint, className = '', ...props }) {
  return (
    <label className={`flex min-w-0 flex-col gap-1.5 ${className}`}>
      <span className="text-[11px] font-extrabold uppercase tracking-[0.09em] text-slate-500">{label}</span>
      <input className="colmena-input h-11" {...props} />
      {hint ? <span className="text-[11px] leading-4 text-muted">{hint}</span> : null}
    </label>
  );
}

function SectionTitle({ icon: Icon, title, description, badge }) {
  return (
    <div className="mb-5 flex flex-wrap items-start justify-between gap-3">
      <div className="flex items-start gap-3">
        <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl bg-gradient-to-br from-[#16383d] to-[#17635f] text-white shadow-sm">
          <Icon size={18} />
        </span>
        <div>
          <h2 className="text-base font-extrabold tracking-tight text-dark">{title}</h2>
          <p className="mt-1 max-w-2xl text-xs leading-5 text-muted">{description}</p>
        </div>
      </div>
      {badge ? <span className="rounded-full bg-turquoise/10 px-3 py-1 text-[10px] font-extrabold uppercase tracking-wider text-turquoise">{badge}</span> : null}
    </div>
  );
}

export default function CompanyProfilePage() {
  const queryClient = useQueryClient();
  const [form, setForm] = useState(() => normalizeProfile(null));
  const [saved, setSaved] = useState(false);

  const profileQuery = useQuery({ queryKey: ['company-profile'], queryFn: getCompanyProfile });
  useEffect(() => {
    if (!profileQuery.isLoading) setForm(normalizeProfile(profileQuery.data));
  }, [profileQuery.data, profileQuery.isLoading]);

  const mutation = useMutation({
    mutationFn: saveCompanyProfile,
    onSuccess: (profile) => {
      queryClient.setQueryData(['company-profile'], profile);
      queryClient.invalidateQueries({ queryKey: ['projects'] });
      setSaved(true);
      window.setTimeout(() => setSaved(false), 2600);
    },
  });

  const completeness = useMemo(() => {
    const required = [form.name, form.legal_name, form.tax_id, form.industry, form.fiscal_address, form.worker_count, form.representative_name, form.study_lead_name, form.contact_email, form.locations?.length];
    return Math.round((required.filter(Boolean).length / required.length) * 100);
  }, [form]);

  const update = (key, value) => setForm((current) => ({ ...current, [key]: value }));
  const updateLocation = (index, key, value) => setForm((current) => ({
    ...current,
    locations: current.locations.map((item, itemIndex) => itemIndex === index ? { ...item, [key]: value } : item),
  }));
  const updateSignatory = (index, key, value) => setForm((current) => ({
    ...current,
    signatories: current.signatories.map((item, itemIndex) => itemIndex === index ? { ...item, [key]: value } : item),
  }));

  const submit = (event) => {
    event.preventDefault();
    mutation.mutate({
      ...form,
      worker_count: Number(form.worker_count),
      locations: form.locations.map((item) => ({ ...item, worker_count: Number(item.worker_count || 0) })),
    });
  };

  if (profileQuery.isLoading) return <LoadingState label="Preparando el perfil de la empresa…" />;
  if (profileQuery.isError) return <ErrorState title="No pudimos cargar la empresa" message={profileQuery.error?.message} />;

  return (
    <form className="colmena-page pb-24" onSubmit={submit}>
      <PageHeader
        eyebrow="Configuración empresarial"
        title="Identidad y alcance de la organización"
        description="Estos datos alimentan las campañas, el expediente técnico y las cuatro secciones de firma. No se mezclan con respuestas de trabajadores."
        actions={<Button type="submit" loading={mutation.isPending}><Save size={15} /> Guardar empresa</Button>}
      />

      <div className="overflow-hidden rounded-[28px] border border-white/20 bg-gradient-to-br from-[#102f33] via-[#173e42] to-[#17635f] p-6 text-white shadow-[0_28px_70px_rgba(16,47,51,.22)] sm:p-8">
        <div className="grid gap-6 lg:grid-cols-[1.3fr_.7fr] lg:items-end">
          <div>
            <span className="inline-flex items-center gap-2 rounded-full border border-white/15 bg-white/10 px-3 py-1.5 text-[10px] font-extrabold uppercase tracking-[0.14em] text-[#9ce8e4]">
              <ShieldCheck size={13} /> Tenant empresarial Colmena
            </span>
            <h1 className="mt-4 max-w-2xl text-2xl font-black tracking-tight sm:text-3xl">Una sola identidad para evaluar, decidir y documentar.</h1>
            <p className="mt-3 max-w-2xl text-sm leading-6 text-white/68">La razón social, población, sedes y responsables se reutilizan automáticamente para evitar reprocesos y errores en cada expediente.</p>
          </div>
          <div className="rounded-2xl border border-white/15 bg-white/10 p-4 backdrop-blur-xl">
            <div className="flex items-center justify-between text-xs"><span className="font-semibold text-white/65">Perfil documental</span><strong>{completeness}%</strong></div>
            <div className="mt-3 h-2 overflow-hidden rounded-full bg-black/20"><div className="h-full rounded-full bg-gradient-to-r from-amber to-[#ffe28b] transition-all" style={{ width: `${completeness}%` }} /></div>
            <p className="mt-3 text-[11px] leading-4 text-white/55">Meta: 100% antes de emitir un expediente para revisión y firma.</p>
          </div>
        </div>
      </div>

      <Card>
        <SectionTitle icon={Building2} title="Identificación legal" description="Información que aparecerá en portada, ficha técnica y control documental." badge="Obligatorio" />
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <Field label="Nombre comercial" value={form.name} onChange={(event) => update('name', event.target.value)} required />
          <Field label="Razón social" value={form.legal_name} onChange={(event) => update('legal_name', event.target.value)} required className="xl:col-span-2" />
          <Field label="RUC" value={form.tax_id} onChange={(event) => update('tax_id', event.target.value.replace(/\D/g, '').slice(0, 11))} inputMode="numeric" minLength={11} maxLength={11} required />
          <Field label="Actividad económica" value={form.industry} onChange={(event) => update('industry', event.target.value)} />
          <Field label="Código CIIU" value={form.ciiu_code || ''} onChange={(event) => update('ciiu_code', event.target.value)} />
          <Field label="Trabajadores" type="number" min="1" value={form.worker_count} onChange={(event) => update('worker_count', event.target.value)} hint="Marco poblacional para cobertura y metas." />
          <Field label="Dirección fiscal" value={form.fiscal_address || ''} onChange={(event) => update('fiscal_address', event.target.value)} className="md:col-span-2 xl:col-span-1" />
        </div>
      </Card>

      <Card>
        <SectionTitle icon={Contact} title="Responsables del proceso" description="Contactos operativos de la evaluación. Las firmas profesionales se configuran de forma separada." />
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <Field label="Representante legal" value={form.representative_name || ''} onChange={(event) => update('representative_name', event.target.value)} />
          <Field label="Responsable del estudio" value={form.study_lead_name || ''} onChange={(event) => update('study_lead_name', event.target.value)} />
          <Field label="Correo SST" type="email" value={form.contact_email || ''} onChange={(event) => update('contact_email', event.target.value)} />
          <Field label="Teléfono" value={form.contact_phone || ''} onChange={(event) => update('contact_phone', event.target.value)} />
        </div>
      </Card>

      <Card>
        <SectionTitle icon={MapPin} title="Sedes y centros de trabajo" description="La suma por sede puede utilizarse como control de cobertura. Los cruces con n < 5 se suprimen en todas las salidas." badge={`${form.locations.length} sedes`} />
        <div className="space-y-3">
          {form.locations.map((location, index) => (
            <div key={`${location.code}-${index}`} className="grid gap-3 rounded-2xl border border-border bg-surfaceSoft/70 p-4 md:grid-cols-[.7fr_1.25fr_1.2fr_.55fr_auto] md:items-end">
              <Field label="Código" value={location.code} onChange={(event) => updateLocation(index, 'code', event.target.value)} />
              <Field label="Sede" value={location.name} onChange={(event) => updateLocation(index, 'name', event.target.value)} />
              <Field label="Ubicación" value={location.address || ''} onChange={(event) => updateLocation(index, 'address', event.target.value)} />
              <Field label="Trabajadores" type="number" min="0" value={location.worker_count} onChange={(event) => updateLocation(index, 'worker_count', event.target.value)} />
              <Button type="button" size="sm" variant="ghost" className="h-11 text-danger" onClick={() => update('locations', form.locations.filter((_, itemIndex) => itemIndex !== index))} aria-label={`Eliminar ${location.name}`}><Trash2 size={16} /></Button>
            </div>
          ))}
          <Button type="button" variant="secondary" size="sm" onClick={() => update('locations', [...form.locations, { code: `SEDE-${form.locations.length + 1}`, name: '', address: '', worker_count: 0 }])}><Plus size={15} /> Agregar sede</Button>
        </div>
      </Card>

      <Card>
        <SectionTitle icon={BadgeCheck} title="Firmantes del expediente" description="Se mantienen cuatro espacios documentales sin crear perfiles adicionales de acceso." badge="4 firmas" />
        <div className="grid gap-3 lg:grid-cols-2">
          {form.signatories.map((signatory, index) => (
            <div key={signatory.role} className="rounded-2xl border border-border bg-white p-4 shadow-sm">
              <div className="mb-3 flex items-center gap-2"><CheckCircle2 size={16} className="text-turquoise" /><p className="text-sm font-bold text-dark">{signatory.role}</p></div>
              <div className="grid gap-3 sm:grid-cols-2">
                <Field label="Nombres y apellidos" value={signatory.full_name} onChange={(event) => updateSignatory(index, 'full_name', event.target.value)} className="sm:col-span-2" />
                <Field label="Cargo / especialidad" value={signatory.position || ''} onChange={(event) => updateSignatory(index, 'position', event.target.value)} />
                <Field label="Colegiatura / registro" value={signatory.professional_id || ''} onChange={(event) => updateSignatory(index, 'professional_id', event.target.value)} />
              </div>
            </div>
          ))}
        </div>
      </Card>

      <Card>
        <SectionTitle icon={Palette} title="Identidad visual" description="Colmena permanece como marca central; este acento se usará de manera secundaria en portadas y detalles." />
        <div className="flex flex-wrap items-center gap-4">
          <input type="color" value={form.brand_color} onChange={(event) => update('brand_color', event.target.value)} className="h-12 w-16 cursor-pointer rounded-xl border border-border bg-white p-1" />
          <div><p className="text-sm font-bold text-dark">Acento corporativo</p><p className="text-xs text-muted">{form.brand_color}</p></div>
          <div className="ml-auto hidden items-center gap-2 rounded-2xl bg-[#102f33] px-4 py-3 text-white sm:flex"><Factory size={18} style={{ color: form.brand_color }} /><span className="text-sm font-bold">{form.name || 'Empresa'}</span><span className="text-[10px] text-white/50">por Colmena</span></div>
        </div>
      </Card>

      {mutation.isError ? <div role="alert" className="rounded-2xl border border-danger/20 bg-danger/10 px-4 py-3 text-sm font-semibold text-danger">{mutation.error?.message || 'No se pudo guardar el perfil.'}</div> : null}
      {saved ? <div className="fixed bottom-6 right-6 z-50 flex items-center gap-2 rounded-2xl bg-[#133c3d] px-4 py-3 text-sm font-bold text-white shadow-2xl"><CheckCircle2 size={17} className="text-[#8fe4dd]" /> Empresa actualizada</div> : null}

      <div className="sticky bottom-4 z-20 ml-auto flex w-fit items-center gap-3 rounded-2xl border border-white/50 bg-white/85 p-2 shadow-xl backdrop-blur-xl">
        <div className="hidden items-center gap-2 px-2 text-xs font-semibold text-muted sm:flex"><Users size={14} /> {form.worker_count || 0} trabajadores</div>
        <Button type="submit" loading={mutation.isPending}><Save size={15} /> Guardar cambios</Button>
      </div>
    </form>
  );
}
