import { useCallback, useEffect, useRef, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

import { useAuth } from '../auth/AuthContext.jsx';
import { BrandMark } from '../brand/BrandMark.jsx';
import { Button } from '../components/ui/Button.jsx';

export default function DemoAccessPage() {
  const { loginDemo } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const attempted = useRef(false);
  const [isEntering, setIsEntering] = useState(true);
  const [accessError, setAccessError] = useState(null);

  const enterDemo = useCallback(async () => {
    setIsEntering(true);
    setAccessError(null);
    try {
      await loginDemo();
      const redirectTo = location.state?.from?.pathname || '/colmena';
      navigate(redirectTo, { replace: true });
    } catch {
      setAccessError('No pudimos iniciar el demo local. Verifica que el servicio Colmena esté activo.');
      setIsEntering(false);
    }
  }, [location.state, loginDemo, navigate]);

  useEffect(() => {
    if (attempted.current) return;
    attempted.current = true;
    enterDemo();
  }, [enterDemo]);

  return (
    <section className="relative flex min-h-screen items-center justify-center overflow-hidden bg-hero-glow px-4 py-6 sm:px-6">
      <div className="colmena-card relative z-10 w-full max-w-md px-6 py-8 text-center sm:px-8 sm:py-10">
        <div className="mx-auto flex flex-col items-center">
          <BrandMark className="h-12 w-12" />
          <span className="mt-5 rounded-full border border-amber/30 bg-amber/10 px-3 py-1 text-[11px] font-bold uppercase tracking-[0.18em] text-amber">
            Demo local
          </span>
          <h1 className="mt-4 text-2xl font-bold text-dark">Bienvenido a Colmena</h1>
          <p className="mt-2 max-w-xs text-sm leading-6 text-muted">
            Preparando el entorno empresarial, la campaña CENSOPAS y su analítica avanzada.
          </p>
        </div>

        <div className="mt-7 rounded-2xl border border-white/70 bg-white/55 px-5 py-5 shadow-inner backdrop-blur-xl">
          {isEntering ? (
            <div className="flex items-center justify-center gap-3 text-sm font-semibold text-dark">
              <span className="h-4 w-4 animate-spin rounded-full border-2 border-teal/25 border-t-teal" />
              Ingresando automáticamente…
            </div>
          ) : (
            <p className="text-sm leading-6 text-danger">{accessError}</p>
          )}
        </div>

        {!isEntering ? (
          <Button type="button" variant="primary" onClick={enterDemo} className="mt-5 w-full">
            Reintentar acceso
          </Button>
        ) : null}

        <p className="mt-5 text-xs leading-5 text-muted">
          Acceso anónimo habilitado únicamente para esta demostración local.
        </p>
      </div>
    </section>
  );
}
