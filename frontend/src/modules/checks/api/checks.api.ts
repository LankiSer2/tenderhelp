import { httpRequest } from "@/shared/api";
import type { CheckListResponse, CreateCheckPayload, SmeCheck } from "@/modules/checks/types";

export function createCheck(payload: CreateCheckPayload): Promise<SmeCheck> {
  return httpRequest<SmeCheck>("/api/checks", {
    method: "POST",
    body: payload,
  });
}

export function listChecks(): Promise<CheckListResponse> {
  return httpRequest<CheckListResponse>("/api/checks");
}
