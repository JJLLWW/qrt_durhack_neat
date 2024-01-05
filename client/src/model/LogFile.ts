export interface ExchangeStats {
    exchange: string;
    order: string;
    recv_nu: number;
    X: number;
}

export interface SourceInfo {
    name: string;
    uuid: string;
}

// NO TIMESTAMP <- field name would be timestamp
export interface LogEntryData {
    status: string;
    message: string;
    stats: ExchangeStats[];
}

export interface LogFile {
    info: SourceInfo;
    entries: LogEntryData[];
}