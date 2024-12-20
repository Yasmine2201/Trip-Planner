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
  avatarUrl: Image | null;
}

export type Error = {
  error_code: string;
  message: string;
}