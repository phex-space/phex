import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import LanguageDetector from "i18next-browser-languagedetector";

import deCommon from "./locales/de/common";
import enCommon from "./locales/en/common";

import deNavigation from "./locales/de/navigation";
import enNavigation from "./locales/en/navigation";

import deSecurity from "./locales/de/security";
import enSecurity from "./locales/en/security";

import deManage from "./locales/de/manage";
import enManage from "./locales/en/manage";

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    interpolation: { escapeValue: false },
    defaultNS: "common",
    resources: {
      de: {
        common: deCommon,
        navigation: deNavigation,
        security: deSecurity,
        manage: deManage,
      },
      en: {
        common: enCommon,
        navigation: enNavigation,
        security: enSecurity,
        manage: enManage,
      },
    },
  });

export default i18n;
