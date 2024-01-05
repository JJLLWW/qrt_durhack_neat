import axios from "axios";

import { LogFile } from "./LogFile";

const base_url = "http://localhost:8000/";

export async function get_all_uuids(): Promise<string[]> {

    const response= await axios.get(`${base_url}/log_files/all_uuids`);
    return response.data;
}

export async function get_file_by_uuid(uuid: string): Promise<LogFile> {
    const response = await axios.get(`${base_url}/log_files/${uuid}`);
    return response.data
}