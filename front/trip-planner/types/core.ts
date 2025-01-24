export type Image = {
  name: string,
  url: string
}

export type User = {
  id: string;
  alias: string;
  firstname: string;
  lastname: string;
  email: string;
  birthdate: string | null;
  avatarImage: Image | null;
  description: string | null;
  languages: string | null;
}

export type Error = {
  error_code: string;
  message: string;
}

export type Page<T> = {
  data: T[];
  current_page: number;
  total_pages: number;
  total_elements: number;
  elements_per_page: number;
}