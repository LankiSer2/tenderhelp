import { onMounted, ref } from "vue";
import { listChecks } from "@/modules/checks/api";
import type { SmeCheck } from "@/modules/checks/types";

export function useChecksHistory() {
  const items = ref<SmeCheck[]>([]);
  const total = ref(0);
  const loading = ref(false);
  const error = ref<string | null>(null);

  async function refresh(): Promise<void> {
    loading.value = true;
    error.value = null;
    try {
      const data = await listChecks();
      items.value = data.items;
      total.value = data.total;
    } catch (err) {
      error.value = err instanceof Error ? err.message : "Не удалось загрузить историю";
    } finally {
      loading.value = false;
    }
  }

  function prepend(check: SmeCheck): void {
    items.value = [check, ...items.value.filter((item) => item.id !== check.id)];
    total.value = Math.max(total.value, items.value.length);
  }

  onMounted(() => {
    void refresh();
  });

  return {
    items,
    total,
    loading,
    error,
    refresh,
    prepend,
  };
}
