import {Typography, Flex, List} from "antd"
import React from "react";

const { Title } = Typography

// does this make sense if may need to filter this, what if table too big to fit on one
// screen
const data = [
    'Racing car sprays burning fuel into crowd.',
    'Japanese princess to wed commoner.',
    'Australian walks 100km after outback crash.',
    'Man charged over missing wedding girl.',
    'Los Angeles battles huge wildfires.'
]

export default function Alerts() {
    return (
        <>
            <Flex vertical={true}>
                <Title level={2}>Alerts</Title>
                <List
                    size="large"
                    bordered={true}
                    dataSource={data}
                    renderItem={(item) => <List.Item>{item}</List.Item>}
                    pagination={false}
                />
            </Flex>
        </>
    )
}