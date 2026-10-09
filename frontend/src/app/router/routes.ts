import type { RouteRecordRaw } from "vue-router";

export const routes: RouteRecordRaw[] = [
  {
    path: "/",
    component: () => import("@/layouts/MainLayout.vue"),
    children: [
      {
        path: "",
        name: "checks",
        component: () => import("@/modules/checks/pages/ChecksPage.vue"),
      },
    ],
  },
];
