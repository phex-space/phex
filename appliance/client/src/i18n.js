import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import LanguageDetector from "i18next-browser-languagedetector";

import deCommon from "./locales/de/common";
import enCommon from "./locales/en/common";

import deNavigation from "./locales/de/navigation";
import enNavigation from "./locales/en/navigation";

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
      },
      en: {
        common: enCommon,
        navigation: enNavigation,
      },
    },
  });

export default i18n;
