export default function BrassPolisher() {
    return (
        <Card>
            <CardHeader>
                <CardTitle>Brass Polisher</CardTitle>
            </CardHeader>
            <CardContent>
                <div className="space-y-4">
                    <select>
                        <option value="brass">Brass</option>
                        <option value="copper">Copper</option>
                        <option value="steel">Steel</option>
                    </select>

                    <div>
                        <label>Polish Intensity</label>
                        <Slider
                            defaultValue={[50]}
                            max={100}
                            step={1}
                        />
                    </div>

                    <div className="preview-area">
                        {}
                    </div>

                    <Button>Apply Polish</Button>
                </div>
            </CardContent>
        </Card>
    )
}