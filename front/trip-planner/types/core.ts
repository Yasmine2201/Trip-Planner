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