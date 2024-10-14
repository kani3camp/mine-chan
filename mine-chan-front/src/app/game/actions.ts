'use server';
import { api } from '@/lib/api';
import {
    ApiGameGameIdGetRequest,
    ApiGamePostRequest,
    ApiGameGameIdDigPostRequest,
    ONOFFApiGameGameIdFlagPostRequest,
} from '@/types/apis';

export const createGame = async (req: ApiGamePostRequest) => {
    return await api.apiGamePost(req);
};

export const getGameById = async (req: ApiGameGameIdGetRequest) => {
    return await api.apiGameGameIdGet(req);
};

export const digByGameId = async (req: ApiGameGameIdDigPostRequest) => {
    return await api.apiGameGameIdDigPost(req);
};

export const onOffFlag = async (req: ONOFFApiGameGameIdFlagPostRequest) => {
    return await api.oNOFFApiGameGameIdFlagPost(req);
};
