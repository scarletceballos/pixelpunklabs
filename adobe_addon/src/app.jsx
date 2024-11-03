import { useState } from 'react';
import { Tabs } from '@/components/ui/tabs';
import TemplateLibrary from './components/TemplateLibrary';
import { BrassPolisher, SteamInfuser, GearConfigurator } from './components/Tools';

export default function App() {
  const [activeTab, setActiveTab] = useState('templates');

  return (
    <div className="container p-4">
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="templates">Templates</TabsTrigger>
          <TabsTrigger value="tools">Tools</TabsTrigger>
        </TabsList>

        <TabsContent value="templates">
          <TemplateLibrary />
        </TabsContent>

        <TabsContent value="tools" className="space-y-4">
          <BrassPolisher />
          <SteamInfuser />
          <GearConfigurator />
        </TabsContent>
      </Tabs>
    </div>
  );
}