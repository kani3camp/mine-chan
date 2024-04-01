import { Configuration, GameApi } from "@/types";

export const api = new GameApi(
    new Configuration({
        basePath: process.env.NEXT_PUBLIC_API_BASE_PATH,
    })
);

