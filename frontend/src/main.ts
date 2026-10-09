import { createApp } from "vue";
import App from "@/app/App.vue";
import { installQuasar } from "@/app/boot/quasar";
import { router } from "@/app/router";

const app = createApp(App);

installQuasar(app);
app.use(router);
app.mount("#app");
