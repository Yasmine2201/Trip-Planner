import type {PublicUser} from "~/types/core";
import type {Trip} from "~/types/trips";

export type Invitation = {
    trip_invitation_id: number,
    status: string,
    trip: Trip,
    sender: PublicUser,
    receiver: PublicUser,
}