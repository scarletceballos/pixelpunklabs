export default function SteamInfuser() {
    return (
        <Card>
            <CardHeader>
                <CardTitle>Steam Infuser</CardTitle>
            </CardHeader>
            <CardContent>
                <div className="space-y-4">
                    <div>
                        <label>Steam Intensity</label>
                        <Silder 
                            defaultValue={[50]}
                            max={100}
                            step={1}
                        />
                    </div>

                    <div className="grid grid-cols-2 gap-2">
                        <div>
                            <label>Density</label>
                            <Slider defaultValue={[70]} />
                        </div>
                        <div>
                            <label>Speed</label>
                            <Slider defaultValue={[50]} />
                        </div>
                    </div>

                    <Button>Add Steam Effect</Button>
                </div>
            </CardContent>
        </Card>
    )
}