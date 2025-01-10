import { z } from 'zod';

export const editProfileSchema = z.object({
  alias: z.string().nonempty({ message: 'errors.alias-required' }),
  firstname: z.string().nonempty({ message: 'errors.first-name-required' }),
  lastname: z.string().nonempty({ message: 'errors.last-name-required' }),
  birthdate: z.string()
    .optional()
    .refine(value => {
      if (!value) return true;
      const birthDate = new Date(value);
      const today = new Date();
      return birthDate <= today;
    }, 'errors.birthdate-invalid'),
  description: z.string().max(1000, { message: 'errors.description-too-long' }),
  // languages: z.array(z.string()).optional(),
});

export type EditProfilDto = z.input<typeof editProfileSchema>;
