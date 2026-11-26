import { getMeApi } from "../api/user.js";
export function useUser() { return { getMe: getMeApi }; }
