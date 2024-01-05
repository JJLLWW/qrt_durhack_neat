import React from 'react';
import {Tabs, Flex, Typography} from 'antd';
import type { TabsProps } from 'antd';

import MainWindow from "./MainWindow";
import Alerts from "./Alerts";
import Stats from "./Stats"

const { Title } = Typography;

const items: TabsProps['items'] = [
    {
        key: '1',
        label: 'File View',
        children: <MainWindow />
    },
    {
        key: '2',
        label: 'Alerts',
        children: <Alerts />
    },
    {
        key: '3',
        label: 'Stats',
        children: <Stats />
    }
];

export default function TabContainer() {
    return (
        <Flex vertical={true}>
            <Title>Log Analyser UI</Title>
            <Tabs defaultActiveKey="1" items={items}/>
        </Flex>
    )
}