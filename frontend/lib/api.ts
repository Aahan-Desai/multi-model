import axios, { AxiosError } from "axios";

import { API_BASE_URL } from "@/lib/constants";

type ApiErrorPayload = {
  detail?: string;
  message?: string;
};

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000,
});

export function getApiErrorMessage(error: unknown) {
  if (axios.isAxiosError<ApiErrorPayload>(error)) {
    return (
      error.response?.data?.detail ??
      error.response?.data?.message ??
      error.message ??
      "Request failed."
    );
  }

  if (error instanceof Error) {
    return error.message;
  }

  return "Something went wrong.";
}

export function isTimeoutError(error: unknown) {
  return (
    error instanceof AxiosError &&
    (error.code === "ECONNABORTED" || error.message.toLowerCase().includes("timeout"))
  );
}
