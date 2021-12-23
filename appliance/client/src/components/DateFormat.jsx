import React, { useState } from "react";
import { useEffect } from "react";
import { useTranslation } from "react-i18next";

const formatters = {};

function getFormatter(language) {
  if (!(language in formatters)) {
    formatters[language] = new Intl.DateTimeFormat(language, {
      dateStyle: "full",
    });
  }
  return formatters[language];
}

function DateFormat({ value }) {
  const { i18n } = useTranslation();
  const formatter = getFormatter(i18n.language);
  const [date, setDate] = useState();
  useEffect(() => {
    if (value instanceof Date) setDate(value);
    else setDate(new Date(value));
  }, [value]);

  return (date && formatter.format(date)) || null;
}

export default DateFormat;
