##! 
##! Copyright(c) 2023 Stanford Research Systems, All rights reserved
##! Subject to the MIT License
##! 

class Keys:
    # Reference component
    Auto = 'auto'
    Internal = 'internal'
    External = 'external'
    Common = 'common'
    Difference = 'difference'
    Dual = 'dual'
    Chop = 'chop'
    Sine = 'sine'
    PositiveTTL = 'positive TTL'
    NegativeTTL = 'negative TTL'
    R50Ohms = '50 Ohms'
    R1Meg = '1 Meg'

    # Signal component
    Voltage = 'voltage'
    Current = 'current'
    AOnly = 'A'
    AMinusB = 'A-B'
    AC = 'AC'
    DC = 'DC'
    Float = 'float'
    Ground = 'ground'
    Off = 'off'
    On = 'on'

    # Output component
    XY = 'XY'
    RT = 'RT'

    X = 'X'
    Y = 'Y'
    R = 'R'
    Theta = 'Theta'

    OutputCh1 = 'OCH1'
    OutputCh2 = 'OCH2'

    # Aux component
    Channel1 = 'CH1'
    Channel2 = 'CH2'
    Channel3 = 'CH3'
    Channel4 = 'CH4'

    # Display component
    Trend = 'trend'
    History = 'history'
    BarHistory = 'bar History'
    FFT = 'FFT'
    BarFFT = 'bar FFT'
    Bar8 = 'bar 8'

    Data1 = 'DAT1'
    Data2 = 'DAT2'
    Data3 = 'DAT3'
    Data4 = 'DAT4'

    AuxInput1 = 'aux in 1'
    AuxInput2 = 'aux in 2'
    AuxInput3 = 'aux in 3'
    AuxInput4 = 'aux in 4'

    XNoise = 'X noise'
    YNoise = 'Y noise'

    AuxOutput1 = 'aux out 1'
    AuxOutput2 = 'aux out 2'

    Phase = 'phase'
    SineOutputAmplitude = 'amplitude'
    DCLevel = 'DC level'
    InternalFrequency = 'int. freq.'
    ExternalFrequency = 'ext. freq.'

    # Chart component
    DateTime = 'date time'
    IntervalTime = 'interval time'

    Mean = 'mean'
    Maximum = 'max'
    Minimum = 'min'

    Line = 'line'
    Narrow = 'narrow'
    Wide = 'wide'

    Status = 'status'

    # FFT component
    ADC = 'ADC'
    MIXER = 'mixer'
    FILTER = 'filter'

    # Scan component
    ReferenceAmplitude = 'reference amplitude'
    ReferenceOffset = 'reference offset'

    Linear = 'linear'
    Log = 'log'

    Once = 'once'
    Repeat = 'repeat'
    UpDown = 'up down'

    Fixed = 'fixed'

    Reset = 'reset'
    Running = 'running'
    Paused = 'paused'
    Done = 'done'

    BEGIN = 'begin'
    END = 'end'

    # DataCapture component
    XYRT = 'XYRT'

    Continuous = 'continuous'
    Immediate = 'immediate'
    TriggerStart = 'trigger start'
    SamplePerTrigger = 'sample per trigger'

    InProgress = 'in progress'
    Triggered = 'triggered'
    Wrapped = 'wrapped'

    # DataStream component
    Float32 = 'float32'
    Int16 = 'int16'
    LittleEndian = 'little endian'
    DataIntegrityChecking = 'data checking'

    # Status component

    ERR = 'ERR'
    LIA = 'LIA'
    MAV = 'MAV'
    ESB = 'ESB'
    SRQ = 'SRQ'

    OPC = 'OPC'
    INP = 'INP'
    QRY = 'QRY'
    EXE = 'EXE'
    CMD = 'CMD'
    URQ = 'URQ'
    PON = 'PON'

    CLK =     'CLK'
    BACKUP =  'BACKUP'
    VXI =     'VXI'
    GPIB =    'GPIB'
    USBDEV =  'USBDEV'
    USBHOST = 'USBHOST'

    CH1OV =  'CH1OV'
    CH2OV =  'CH2OV'
    UNLK =   'UNLK'
    RANGE =  'RANGE'
    SYNCF =  'SYNCF'
    SYNCOV = 'SYNCOV'
    TRIG =   'TRIG'
    DAT1OV = 'DAT1OV'
    DAT2OV = 'DAT2OV'
    DAT3OV = 'DAT3OV'
    DAT4OV = 'DAT4OV'
    DCAPFIN = 'DCAPFIN'
    SCNST =  'SCNST'
    SCNFIN = 'SCNFIN'

    Ch1OutputScale = 'ch1 output scale'
    Ch2OutputScale = 'ch2 output scale'
    ExternalReferenceUnlocked = 'external reference unlocked'
    InputRange = 'input range'
    DataCh1Scale = 'data CH1 scale'
    DataCh2Scale = 'data cH2 scale'
    DataCh3Scale = 'data cH3 scale'
    DataCh4Scale = 'data cH4 scale'
