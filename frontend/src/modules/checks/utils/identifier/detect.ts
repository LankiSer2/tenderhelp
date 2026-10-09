import type { IdentifierType } from "@/modules/checks/types";
import { isInnChecksumValid, isOgrnChecksumValid } from "./checksum";
import { normalizeIdentifier } from "./normalize";

export function detectIdentifierType(raw: string): IdentifierType {
  const value = normalizeIdentifier(raw);

  if ((value.length === 10 || value.length === 12) && isInnChecksumValid(value)) {
    return "INN";
  }
  if ((value.length === 13 || value.length === 15) && isOgrnChecksumValid(value)) {
    return "OGRN";
  }
  if (value.length === 10 || value.length === 12) {
    return "INN";
  }
  if (value.length === 13 || value.length === 15) {
    return "OGRN";
  }
  return "UNKNOWN";
}

export function isIdentifierReady(raw: string): boolean {
  const type = detectIdentifierType(raw);
  return type === "INN" || type === "OGRN";
}
