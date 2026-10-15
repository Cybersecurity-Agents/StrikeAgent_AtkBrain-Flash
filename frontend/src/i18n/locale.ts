export type Locale = "zh" | "en";

export const LOCALE_KEY = "atkbrain_locale";

const listeners = new Set<() => void>();
let current: Locale = "zh";

export function normalizeLocale(raw: string | null | undefined): Locale {
  const s = String(raw || "").trim().toLowerCase().replace("_", "-");
  if (s.startsWith("en")) return "en";
  return "zh";
}

export function detectLocale(): Locale {
  return "zh";
}

export function getLocale(): Locale {
  return current;
}

export function applyDocumentLocale(locale: Locale) {
  if (typeof document === "undefined") return;
  document.documentElement.lang = locale === "en" ? "en" : "zh-CN";
  document.title = locale === "en"
    ? "StrikeAgent_AtkBrain-Flash · Red-team AI pentest platform"
    : "StrikeAgent_AtkBrain-Flash · 红队 AI 渗透平台";
}

export function setLocale(_next: Locale) {
  current = "zh";
  try {
    localStorage.setItem(LOCALE_KEY, "zh");
  } catch {
    /* ignore */
  }
  applyDocumentLocale("zh");
  listeners.forEach((fn) => fn());
}

export function subscribeLocale(fn: () => void): () => void {
  listeners.add(fn);
  return () => { listeners.delete(fn); };
}

current = "zh";
try {
  localStorage.setItem(LOCALE_KEY, "zh");
} catch {
  /* ignore */
}
applyDocumentLocale(current);
