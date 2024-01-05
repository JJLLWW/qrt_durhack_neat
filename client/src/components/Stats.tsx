import React from 'react'
import {Tabs, Flex, Typography} from "antd";
import {data} from '../test_data/log_file'

const { Title, Text } = Typography;

// react-google-charts
export default function Stats() {
    return (
        <Flex vertical={true}>
            <Title level={2}>Stats</Title>
            <Text>{JSON.stringify(data.entries)}</Text>
        </Flex>
    )
}