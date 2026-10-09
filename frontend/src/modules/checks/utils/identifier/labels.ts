import type { IdentifierType } from "@/modules/checks/types";

export function identifierLabel(type: IdentifierType): string {
  switch (type) {
    case "INN":
      return "ИНН";
    case "OGRN":
      return "ОГРН / ОГРНИП";
    default:
      return "не определено";
  }
}
