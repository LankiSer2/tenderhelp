import { computed, ref, type Ref } from "vue";
import type { IdentifierType } from "@/modules/checks/types";
import {
  detectIdentifierType,
  identifierLabel,
  isIdentifierReady,
  normalizeIdentifier,
} from "@/modules/checks/utils";

export function useIdentifierDetection(source?: Ref<string>) {
  const query = source ?? ref("");

  const identifierType = computed<IdentifierType>(() => detectIdentifierType(query.value));
  const label = computed(() => identifierLabel(identifierType.value));
  const normalized = computed(() => normalizeIdentifier(query.value));
  const ready = computed(() => isIdentifierReady(query.value));

  return {
    query,
    identifierType,
    label,
    normalized,
    ready,
  };
}
