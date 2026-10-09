import { Quasar, Notify, Dialog, Loading } from "quasar";
import type { App } from "vue";

import "@quasar/extras/material-icons/material-icons.css";
import "quasar/src/css/index.sass";
import "@/css/app.scss";

export function installQuasar(app: App): void {
  app.use(Quasar, {
    plugins: {
      Notify,
      Dialog,
      Loading,
    },
  });
}
