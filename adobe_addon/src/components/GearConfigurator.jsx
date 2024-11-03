export default function GearConfigurator() {
    return (
        <Card>
            <CardHeader>
                <CardTitle>Gear Configuration</CardTitle>
            </CardHeader>
            <CardContent>
                <div className="spece-y-4">
                    <div>
                        <label>Complexity</label>
                        <Slider 
                            defaultValue={[1]}
                            max={3}
                            step={1}
                        />
                    </div>

                    <div className="design-area min-h-[200px] border rounded">
                        {}
                    </div>

                    <div className="flex gap-2">
                        <Button>Add Gear</Button>
                        <Button>Connect Gears</Button>
                        <Button>Generate System</Button>
                    </div>
                </div>
            </CardContent>
        </Card>
    )
}