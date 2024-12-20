import {z} from "zod";

export const loginSchema = z.object({
  email: z.string().nonempty({message: 'errors.email-required'}).email({message: 'errors.email-invalid'}),
  password: z.string().nonempty({message: 'errors.password-required'})
});

export type LoginDto = z.input<typeof loginSchema>;