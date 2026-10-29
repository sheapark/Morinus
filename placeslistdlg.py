import wx
import geonames
import mtexts
import util


class PlaceListCtrl(wx.ListCtrl):
    PLACE = 0
    COUNTRY = 1
    LON = 2
    LAT = 3
    ZONE = 4
    ALT = 5
    COLNUM = ALT + 1

    def __init__(self, parent, li, ID, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        self.placedata = {}
        self.load(li)
        self.Populate()
        self.changed = False

    def Populate(self):
        self.InsertColumn(PlaceListCtrl.PLACE, mtexts.txts['Place'])
        self.InsertColumn(PlaceListCtrl.COUNTRY, mtexts.txts['Country'])
        self.InsertColumn(PlaceListCtrl.LON, mtexts.txts['Long'] + '.')
        self.InsertColumn(PlaceListCtrl.LAT, mtexts.txts['Lat'] + '.')
        self.InsertColumn(PlaceListCtrl.ZONE, mtexts.txts['Zone'])
        self.InsertColumn(PlaceListCtrl.ALT, mtexts.txts['Alt'] + '.')

        for key in sorted(self.placedata.keys()):
            data = self.placedata[key]
            index = self.InsertItem(self.GetItemCount(), data[0])
            for col in range(1, PlaceListCtrl.COLNUM):
                self.SetItem(index, col, data[col])
            self.SetItemData(index, key)

        self.SetColumnWidth(PlaceListCtrl.PLACE, 160)
        self.SetColumnWidth(PlaceListCtrl.COUNTRY, 130)
        self.SetColumnWidth(PlaceListCtrl.LON, 70)
        self.SetColumnWidth(PlaceListCtrl.LAT, 70)
        self.SetColumnWidth(PlaceListCtrl.ZONE, 70)
        self.SetColumnWidth(PlaceListCtrl.ALT, 60)

        self.currentItem = -1
        if len(self.placedata):
            self.currentItem = 0
            self.SetItemState(0, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)

    def OnItemSelected(self, event):
        self.currentItem = event.GetIndex()
        event.Skip()

    def load(self, li):
        idx = 0
        for it in li:
            dirtxt = 'E'
            lon = it[geonames.Geonames.LON]
            if lon < 0.0:
                dirtxt = 'W'
                lon *= -1
            d, m, s = util.decToDeg(lon)
            lontxt = str(d).zfill(2) + dirtxt + str(m).zfill(2)

            dirtxt = 'N'
            lat = it[geonames.Geonames.LAT]
            if lat < 0.0:
                dirtxt = 'S'
                lat *= -1
            d, m, s = util.decToDeg(lat)
            lattxt = str(d).zfill(2) + dirtxt + str(m).zfill(2)

            gmtoffs = it[geonames.Geonames.GMTOFFS]
            signtxt = '+'
            if gmtoffs < 0.0:
                signtxt = '-'
                gmtoffs *= -1
            frac = int(round((gmtoffs - int(gmtoffs)) * 60.0))
            gmtoffstxt = signtxt + str(int(gmtoffs)) + ':' + str(frac).zfill(2)

            self.placedata[idx] = (str(it[geonames.Geonames.NAME]), str(it[geonames.Geonames.COUNTRYNAME]),
                                   lontxt, lattxt, gmtoffstxt, str(it[geonames.Geonames.ALTITUDE]))
            idx += 1


class PlacesListDlg(wx.Dialog):

    def __init__(self, parent, li):
        wx.Dialog.__init__(self, parent, -1, mtexts.txts['Places'], pos=wx.DefaultPosition,
                           size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        mvsizer = wx.BoxSizer(wx.VERTICAL)

        ID_Places = wx.NewIdRef()
        self.li = PlaceListCtrl(self, li, ID_Places, size=(580, 230),
                                style=wx.LC_VRULES | wx.LC_REPORT | wx.LC_SINGLE_SEL)
        mvsizer.Add(self.li, 1, wx.GROW | wx.ALL, 10)
        self.li.Bind(wx.EVT_LIST_ITEM_ACTIVATED, lambda e: self.EndModal(wx.ID_OK))

        btnsizer = wx.StdDialogButtonSizer()
        btnOk = wx.Button(self, wx.ID_OK, mtexts.txts['Ok'])
        btnOk.SetDefault()
        btnsizer.AddButton(btnOk)
        btnCancel = wx.Button(self, wx.ID_CANCEL, mtexts.txts['Cancel'])
        btnsizer.AddButton(btnCancel)
        btnsizer.Realize()

        mvsizer.Add(btnsizer, 0, wx.GROW | wx.ALL, 10)
        self.SetSizer(mvsizer)
        mvsizer.Fit(self)
        btnOk.SetFocus()
