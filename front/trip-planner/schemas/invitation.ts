import {z} from "zod";

export const invitationSchema = z.object({
  alias: z.string().min(1, {message: 'errors.alias-required'}),
})