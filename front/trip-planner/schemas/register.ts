import { z } from "zod";

export const registerSchema = z.object({
  firstName: z.string().nonempty({ message: 'errors.first-name-required' }),
  lastName: z.string().nonempty({ message: 'errors.last-name-required' }),
  alias: z.string().nonempty({ message: 'errors.alias-required' }),
  birthdate: z.string()
    .optional()
    .refine(value => {
      if (!value) return true;
      const birthDate = new Date(value);
      const today = new Date();
      return birthDate <= today;
    }, 'errors.birthdate-invalid'),
  email: z.string()
    .nonempty({ message: 'errors.email-required' })
    .email({ message: 'errors.email-invalid' }),
  password: z.string()
    .nonempty({ message: 'errors.password-required' }),
  confirmPassword: z.string()
    .nonempty({ message: 'errors.confirm-password-required' })
  }
).refine(data => data.password === data.confirmPassword, {
  message: 'errors.passwords-must-match',
  path: ['confirmPassword']
});

export type RegisterDto = z.input<typeof registerSchema>;
