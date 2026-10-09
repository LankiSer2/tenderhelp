export function normalizeIdentifier(value: string): string {
  return value.replace(/\D/g, "");
}
