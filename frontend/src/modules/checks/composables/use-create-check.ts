import { ref } from "vue";
import { createCheck } from "@/modules/checks/api";
import type { SmeCheck } from "@/modules/checks/types";

export function useCreateCheck() {
  const loading = ref(false);
  const error = ref<string | null>(null);
  const result = ref<SmeCheck | null>(null);

  async function submit(query: string): Promise<SmeCheck | null> {
    loading.value = true;
    error.value = null;

    try {
      const check = await createCheck({ query });
      result.value = check;
      return check;
    } catch (err) {
      error.value = err instanceof Error ? err.message : "Не удалось выполнить проверку";
      return null;
    } finally {
      loading.value = false;
    }
  }

  return {
    loading,
    error,
    result,
    submit,
  };
}
