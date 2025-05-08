
import FactorTester as ft
import ManageData as md
import TransformData as td


SaveFile    = 'DataHighCap.pkl'   
D           = md.loadproject(SaveFile)

TransformList   = ['ZSBT']
Signal          =   td.Transform(D['FCF_Price_AP'],TransformList,D)
Returns     =   D['Returns_AP']
SignalName  =   'FCF_PriceZSBT'
NumTile     =   5
R           =   ft.AnalyzeFactor(SignalName,Signal,Returns,NumTile)
