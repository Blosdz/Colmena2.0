import { useId } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import {
  ChevronRight,
  FileQuestion,
  FolderKanban,
  GraduationCap,
  Layers3,
  Plus,
  Search,
  SlidersHorizontal,
  Users,
} from 'lucide-react';

import { createProject } from '../../../api/projects.js';
import { cn } from '../../../utils/cn.js';
import { Button } from '../../ui/Button.jsx';
import FormField from '../../ui/FormField.jsx';
import { Modal } from '../../ui/Modal.jsx';

const PROJECT_TYPES = [
  { value: 'ACADEMIC', label: 'Académico', description: 'Tesis de grado, maestría o doctorado.', icon: GraduationCap },
  { value: 'CENSO', label: 'Evaluación psicosocial', description: 'Campaña CENSOPAS-COPSOQ con resultados colectivos y medidas preventivas.', icon: Users },
  { value: 'RESEARCH', label: 'Investigación', description: 'Estudios científicos o institucionales.', icon: Search },
  { value: 'CUSTOM', label: 'Personalizado', description: 'Una estructura adaptada a tu caso.', icon: SlidersHorizontal },
];

const schema = z.object({
  name: z.string().trim().min(1, 'Ingresa un nombre').max(255, 'Usa 255 caracteres como máximo'),
  projectType: z.enum(['ACADEMIC', 'CENSO', 'RESEARCH', 'CUSTOM']),
  description: z.string().trim().max(1000, 'Usa 1000 caracteres como máximo').optional(),
});

const campaignSchema = schema.extend({
  workerCount: z.coerce.number().int().min(1, 'Indica al menos un trabajador').max(100000).optional(),
  instrumentVersion: z.enum(['SHORT', 'MEDIUM']).optional(),
});
export default function ProjectCreateModal({ ownerUserId, onClose, onCreated }) {
  const formId = useId();
  const queryClient = useQueryClient();
  const {
    register,
    handleSubmit,
    setValue,
    watch,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(campaignSchema),
    defaultValues: { name: '', projectType: 'CENSO', description: '', workerCount: 24, instrumentVersion: 'SHORT' },
  });

  const selectedType = watch('projectType');
  const mutation = useMutation({
    mutationFn: (values) => createProject({
      ownerUserId,
      name: values.name,
      projectType: values.projectType,
      description: values.description,
      metadata: values.projectType === 'CENSO' ? {
        product_mode: 'PSYCHOSOCIAL',
        methodology: 'CENSOPAS_COPSOQ',
        methodology_mode: 'COLMENA_EXPLORATORY',
        instrument_version_kind: values.instrumentVersion,
        expected_worker_count: Number(values.workerCount),
        min_publishable_n: 5,
        anonymity_mode: 'ANONYMOUS_LINK',
        official_equivalence_enabled: false,
        campaign_status: 'DRAFT',
      } : {},
    }),
    onSuccess: (project) => {
      queryClient.invalidateQueries({ queryKey: ['projects'] });
      queryClient.invalidateQueries({ queryKey: ['archive-projects'] });
      queryClient.invalidateQueries({ queryKey: ['sidebar-projects'] });
      if (onCreated) onCreated(project);
      else onClose();
    },
  });

  return (
    <Modal
      title="Crear proyecto"
      subtitle="Elige el contexto y Colmena preparará la estructura metodológica inicial."
      icon={FolderKanban}
      onClose={onClose}
      size="lg"
      preventClose={mutation.isPending}
      footer={
        <>
          <Button type="button" variant="secondary" size="lg" onClick={onClose} disabled={mutation.isPending}>
            Cancelar
          </Button>
          <Button
            type="submit"
            form={formId}
            size="lg"
            loading={mutation.isPending}
            className="bg-gradient-to-r from-amber to-honey px-6 text-white shadow-soft hover:opacity-95"
          >
            <Plus size={16} />
            Crear proyecto
          </Button>
        </>
      }
    >
      <form id={formId} className="space-y-5" onSubmit={handleSubmit((values) => mutation.mutate(values))} noValidate>
        <FormField
          label="Nombre del proyecto"
          placeholder="Ej. Tesis de satisfacción académica"
          error={errors.name?.message}
          autoFocus
          autoComplete="off"
          {...register('name')}
        />

        <fieldset>
          <legend className="colmena-label mb-2">Tipo de proyecto</legend>
          <input type="hidden" {...register('projectType')} />
          <div className="grid gap-2 sm:grid-cols-2">
            {PROJECT_TYPES.map((type) => {
              const TypeIcon = type.icon;
              const selected = selectedType === type.value;
              return (
                <button
                  key={type.value}
                  type="button"
                  aria-pressed={selected}
                  onClick={() => setValue('projectType', type.value, { shouldValidate: true })}
                  className={cn(
                    'flex items-start gap-3 rounded-xl border p-3 text-left transition focus:outline-none focus:ring-2 focus:ring-amber/30',
                    selected
                      ? 'border-amber bg-amber/10 shadow-sm'
                      : 'border-border bg-white hover:border-amber/40 hover:bg-yellowSoft/50',
                  )}
                >
                  <span className={cn('flex h-9 w-9 shrink-0 items-center justify-center rounded-lg', selected ? 'bg-white text-amber' : 'bg-surfaceSoft text-muted')}>
                    <TypeIcon size={18} />
                  </span>
                  <span>
                    <span className="block text-sm font-semibold text-dark">{type.label}</span>
                    <span className="mt-0.5 block text-xs leading-4 text-muted">{type.description}</span>
                  </span>
                </button>
              );
            })}
          </div>
        </fieldset>

        <label className="flex flex-col gap-2">
          <span className="colmena-label">Descripción (opcional)</span>
          <textarea
            rows={3}
            placeholder="Resume el propósito y la población de estudio."
            className={cn(
              'min-h-[88px] resize-y rounded-xl border bg-white px-3 py-2.5 text-sm text-dark outline-none transition placeholder:text-muted focus:border-amber focus:ring-2 focus:ring-amber/15',
              errors.description ? 'border-danger' : 'border-border',
            )}
            {...register('description')}
          />
          {errors.description ? <span className="text-xs font-medium text-danger">{errors.description.message}</span> : null}
        </label>

        {selectedType === 'CENSO' ? (
          <section className="space-y-3 rounded-2xl border border-turquoise/20 bg-gradient-to-br from-turquoise/10 via-white to-amber/5 p-4">
            <div className="flex items-start gap-3">
              <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-turquoise text-white"><Users size={18} /></span>
              <div>
                <p className="text-sm font-bold text-dark">Configuracion CENSOPAS-COPSOQ</p>
                <p className="mt-1 text-xs leading-5 text-muted">Demo sintetico para mineria. La empresa vera resultados colectivos, no respuestas individuales.</p>
              </div>
            </div>
            <div className="grid gap-3 sm:grid-cols-2">
              <FormField
                label="Trabajadores estimados"
                type="number"
                min="1"
                error={errors.workerCount?.message}
                {...register('workerCount')}
              />
              <label className="flex flex-col gap-2">
                <span className="colmena-label">Version del cuestionario</span>
                <select className="colmena-input" {...register('instrumentVersion')}>
                  <option value="SHORT">Corta - 42 preguntas / 6 dimensiones</option>
                  <option value="MEDIUM">Media - 112 preguntas / 20 subdimensiones</option>
                </select>
              </label>
            </div>
            <p className="rounded-xl border border-turquoise/20 bg-white/75 px-3 py-2 text-xs leading-5 text-muted">
              Recomendacion: {Number(watch('workerCount')) >= 25 ? 'version media para una lectura por subdimensiones.' : 'version corta para centros pequenos.'}
            </p>
            <p className="rounded-xl border border-dark/10 bg-dark px-3 py-2 text-xs leading-5 text-white/75">
              Enlace anonimo, sin nombre, DNI ni correo junto a las respuestas. Se suprimen grupos menores de 5 personas.
            </p>
          </section>
        ) : null}

        <div className="rounded-2xl border border-amber/20 bg-yellowSoft/70 p-4">
          <p className="mb-3 text-xs font-semibold uppercase tracking-[0.12em] text-yellowDark">Estructura del proyecto</p>
          <div className="flex flex-wrap items-center gap-2">
            {[
              [FolderKanban, 'Proyecto'],
              [Layers3, 'Variables'],
              [SlidersHorizontal, 'Dimensiones'],
              [FileQuestion, 'Preguntas'],
            ].map(([StepIcon, label], index) => (
              <div key={label} className="contents">
                <span className="inline-flex items-center gap-1.5 rounded-xl border border-border bg-white px-2.5 py-2 text-xs font-semibold text-dark shadow-sm">
                  <StepIcon size={14} className="text-amber" />
                  {label}
                </span>
                {index < 3 ? <ChevronRight size={14} className="text-amber" /> : null}
              </div>
            ))}
          </div>
        </div>

        {mutation.isError ? (
          <p role="alert" className="rounded-xl border border-danger/20 bg-danger/10 px-3 py-2.5 text-sm font-medium text-danger">
            {mutation.error?.message || 'No se pudo crear el proyecto.'}
          </p>
        ) : null}
      </form>
    </Modal>
  );
}
