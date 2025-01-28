type PublicUser = {
    user_id: string,
    alias: string,
    first_name: string,
    profile_picture: string,
    description: string,
    languages: string
}
type Trip = {
    trip_id: number
    trip_name: string
    start_date: string
    end_date: string
    latitude: number
    longitude: number
    radius: number
}
export type Invitation = {
    trip_invitation_id: number,
    status: string,
    trip: Trip,
    sender: PublicUser,
    receiver: PublicUser,
}