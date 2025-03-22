import { axiosAuth } from "@/app/lib/axios";

export interface RegisterPayload {
  username: string;
  email: string;
  password: string;
  profile_picture?: string;
  biography?: string;
}

export async function registerUser(payload: RegisterPayload) {
  const response = await axiosAuth.post("/registro", payload);
  return response.data;
}
