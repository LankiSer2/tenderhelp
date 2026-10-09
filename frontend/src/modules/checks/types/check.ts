export type IdentifierType = "INN" | "OGRN" | "UNKNOWN";

export interface SmeCheck {
  id: string;
  identifier: string;
  identifier_type: IdentifierType | string;
  is_sme: boolean;
  sme_category: string | null;
  company_name: string | null;
  inn: string | null;
  ogrn: string | null;
  from_cache: boolean;
  created_at: string;
}

export interface CheckListResponse {
  items: SmeCheck[];
  total: number;
}

export interface CreateCheckPayload {
  query: string;
}
