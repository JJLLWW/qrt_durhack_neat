import { Button, Table, Select, Flex, Typography, Modal, Input, Space } from "antd";
import React, { useState } from "react";
import type { ColumnsType} from "antd/es/table";
import { SearchOutlined } from '@ant-design/icons';
import {data as Data} from '../test_data/log_file'

const { Title } = Typography;

type StatFilter = 'with_stats' | 'without_stats'

interface FilterState {
    allowed_statuses?: string[];
    message_regex?: string;
    stat_filter?: StatFilter;
    time_start?: string;
    time_end?: string;
}

interface DataType {
    key: string;
    timestamp: string;
    status: string;
    message: string;
    stats: string;
}

function dataFromEntry(entry: any, i: number)  {
    let res = {key: `${i}`, ...entry}
    res.stats = "NONE"
    return res
}

const data = Data.entries.map((ent: any, i:number) => { return dataFromEntry(ent, i) })
// how would highlighting work? <- react-highlight-words library
// only want regex search on the message, some kind of time interval for timestamp?
// filterDropdown?
// store the filter state in some object?
export default function MainWindow() {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [filterState, setFilterState] = useState<FilterState>({});

    const handleCancel = () => {
        setIsModalOpen(false);
    }

    const handleStatsClick = () => {
        setIsModalOpen(true);
    }

    const columns: ColumnsType<DataType> = [
        {
            title: 'Timestamp',
            dataIndex: 'timestamp',
            key: 'timestamp',
            width: '20%',
            filterDropdown: ({ setSelectedKeys, selectedKeys, confirm, clearFilters, close }) => {
                return <div style={{padding: 8}}>
                    <Input placeholder="TIME_FROM" style={{marginBottom: 8}} />
                    <Input placeholder="TIME_TO" style={{marginBottom: 8}} />
                    <Space>
                        <Button
                            type="primary"
                            onClick={() => {confirm()}}
                            icon={<SearchOutlined />}
                            size="small"
                            style={{ width: 90 }}
                        >
                            Search
                        </Button>
                        <Button
                            onClick={() => {clearFilters && clearFilters(); setSelectedKeys([])}}
                            size="small"
                            style={{ width: 90 }}
                        >
                            Reset
                        </Button>
                    </Space>
                </div>
            },
            onFilter: (value: any, record: DataType) => {
                return true;
            }
        },
        {
            title: 'Status',
            dataIndex: 'status',
            filters: [
                {text: 'INFO', value: 'INFO'},
                {text: 'DEBUG', value: 'DEBUG'}
            ],
            key: 'status',
            width: "5%",
            onFilter: (value: any, record: DataType) => {
                return record.status === value;
            }
        },
        {
            title: 'Message',
            dataIndex: 'message',
            key: 'message',
            ellipsis: true,
            filterDropdown: ({ setSelectedKeys, selectedKeys, confirm, clearFilters, close }) => {
                return <div style={{ padding: 8 }}>
                    <Input
                        placeholder={'Filter By Regex'}
                        value={selectedKeys[0]}
                        onChange={(e) => setSelectedKeys(e.target.value ? [e.target.value] : [])}
                        style={{marginBottom: 8}}
                    />
                    <Space>
                        <Button
                            type="primary"
                            onClick={() => {confirm()}}
                            icon={<SearchOutlined />}
                            size="small"
                            style={{ width: 90 }}
                        >
                            Search
                        </Button>
                        <Button
                            onClick={() => {clearFilters && clearFilters(); setSelectedKeys([])}}
                            size="small"
                            style={{ width: 90 }}
                        >
                            Reset
                        </Button>
                    </Space>
                </div>
            },
            onFilter: (value: any, record: DataType) => {
                return record.message.includes(value)
            }
        },
        {
            title: 'Stats',
            dataIndex: 'stats',
            filters: [
                {text: 'STATS_ONLY', value: 'WITH_STATS'}
            ],
            key: 'stats',
            width: '10%',
            align: 'center',
            onFilter: (value: any, record: DataType) => {
                if(value === 'WITH_STATS') {
                    return record.stats !== 'NONE';
                } else {
                    return true;
                }
            },
            render: (_: any, record: DataType) => {
                return (
                    record.stats === 'NONE' ?
                        <div>None</div> :
                        <Button onClick={handleStatsClick} type="link">Display Stats</Button>
                )
            }
        }
    ]

    return (
        <>
            <Flex vertical={true}>
                <Title level={2}>File View</Title>
                <Select
                    placeholder={"Choose Log File"}
                    onChange={(value: string) => {}}
                    options={[
                        {value: "A", label: "A"},
                        {value: "B", label: "B"}
                    ]}
                    style={{marginBottom: 8}}
                />
                <Table
                    dataSource={data}
                    columns={columns}
                    pagination={false}
                    scroll={{y: 600}}
                    style={{marginBottom: 8}}
                />
                <Modal
                    title="Stats Info at 24/5/23 13:20:45.213789"
                    width="80%"
                    open={isModalOpen}
                    onCancel={handleCancel}
                    footer={null}
                >
                    <Table dataSource={data} columns={columns} />
                </Modal>
                <Space>
                    <Button type="primary">SAVE FILTER STATE</Button>
                    <Select placeholder="CHOOSE SAVED FILTER" options={[
                        {value: "A", label: "A"},
                        {value: "B", label: "B"}]
                    }/>
                    <Input
                        placeholder="HIGHLIGHT BY REGEX"
                    />
                </Space>
            </Flex>
        </>
    )
}