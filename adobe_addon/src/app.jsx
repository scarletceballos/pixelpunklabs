import React from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import BrassPolisher from './components/BrassPolisher';
import SteamInfuser from './components/SteamInfuser';
import GearConfigurator from './components/GearConfigurator';
import TemplateLibrary from './components/TemplateLibrary';
import { useAddOnSdk } from './hooks/useAddOnSdk';

const App = () => {
  const { addOnSdk } = useAddOnSdk();

  return (
    <Card className="w-full max-w-md">
      <CardHeader>
        <CardTitle>Steampunk Design Toolkit</CardTitle>
        <CardDescription>
          Create Victorian-era designs with mechanical flair
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="templates" className="w-full">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="templates">Templates</TabsTrigger>
            <TabsTrigger value="tools">Modification Tools</TabsTrigger>
          </TabsList>
          
          <TabsContent value="templates">
            <TemplateLibrary addOnSdk={addOnSdk} />
          </TabsContent>
          
          <TabsContent value="tools">
            <div className="space-y-6">
              <BrassPolisher addOnSdk={addOnSdk} />
              <SteamInfuser addOnSdk={addOnSdk} />
              <GearConfigurator addOnSdk={addOnSdk} />
            </div>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  );
};

export default App;