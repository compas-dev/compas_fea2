"""
********************************************************************************
Ansys
********************************************************************************
"""

from pydoc import ErrorDuringImport
import compas_fea2

from compas.plugins import plugin

# Models
from compas_fea2.model import Model
from compas_fea2.model import DeformablePart
from compas_fea2.model import Node
# Elements
from compas_fea2.model.elements import (
    MassElement,
    BeamElement,
    TrussElement,
    MembraneElement,
    ShellElement,
    _Element3D,
)
# Sections
from compas_fea2.model.sections import (
    AngleSection,
    BeamSection,
    BoxSection,
    CircularSection,
    HexSection,
    ISection,
    MassSection,
    PipeSection,
    RectangularSection,
    SpringSection,
    StrutSection,
    TieSection,
    TrapezoidalSection,
    TrussSection,
    MembraneSection,
    ShellSection,
    SolidSection,
)
# Materials
from compas_fea2.model.materials import (
    ElasticIsotropic,
    ElasticOrthotropic,
    ElasticPlastic,
    Stiff,
    UserMaterial,
    Concrete,
    ConcreteDamagedPlasticity,
    ConcreteSmearedCrack,
    Steel,
)
# Groups
from compas_fea2.model.groups import (
    NodesGroup,
    ElementsGroup,
    FacesGroup,
)

# Constraints
from compas_fea2.model.constraints import (
    TieConstraint,
)
# Releases
from compas_fea2.model.releases import (
    BeamEndPinRelease,
)

# Boundary Conditions
from compas_fea2.model.bcs import (
    FixedBC,
    ClampBCXX,
    ClampBCYY,
    ClampBCZZ,
    PinnedBC,
    RollerBCX,
    RollerBCXY,
    RollerBCXZ,
    RollerBCY,
    RollerBCYZ,
    RollerBCZ,
)

# Problem
from compas_fea2.problem import Problem
# Steps
from compas_fea2.problem.steps import (
    ModalAnalysis,
    ComplexEigenValue,
    StaticStep,
    LinearStaticPerturbation,
    BucklingAnalysis,
    DynamicStep,
    QuasiStaticStep,
    DirectCyclicStep,
)
# Loads
from compas_fea2.problem.loads import (
    PointLoad,
    LineLoad,
    AreaLoad,
    TributaryLoad,
    PrestressLoad,
    GravityLoad,
    HarmonicPointLoad,
    HarmonicPressureLoad,
)
# Displacements
from compas_fea2.problem.displacements import (
    GeneralDisplacement,
)
# Outputs
from compas_fea2.problem.outputs import (
    FieldOutput,
    HistoryOutput,
)

# Results
from compas_fea2.results import (
    Results
)

# Input File
from compas_fea2.job import (
    InputFile,
    ParametersFile,
)
# =========================================================================
#                           ANSYS CLASSES
# =========================================================================

try:
    # Ansys Models
    from .model import AnsysModel
    from .model import AnsysPart
    from .model import AnsysNode

    # Ansys Elements
    from .model.elements import (
        AnsysMassElement,
        AnsysBeamElement,
        AnsysTrussElement,
        AnsysMembraneElement,
        AnsysShellElement,
        _AnsysElement3D,
    )

    # Ansys Sections
    from .model.sections import (
        AnsysAngleSection,
        AnsysBeamSection,
        AnsysBoxSection,
        AnsysCircularSection,
        AnsysHexSection,
        AnsysISection,
        AnsysMassSection,
        AnsysPipeSection,
        AnsysRectangularSection,
        AnsysSpringSection,
        AnsysStrutSection,
        AnsysTieSection,
        AnsysTrapezoidalSection,
        AnsysTrussSection,
        AnsysMembraneSection,
        AnsysShellSection,
        AnsysSolidSection,
    )

    # Ansys Materials
    from .model.materials import (
        AnsysElasticIsotropic,
        AnsysElasticOrthotropic,
        AnsysElasticPlastic,
        AnsysStiff,
        AnsysUserMaterial,
        AnsysConcrete,
        AnsysConcreteDamagedPlasticity,
        AnsysConcreteSmearedCrack,
        AnsysSteel,
    )

    # Ansys Groups
    from .model.groups import (
        AnsysNodesGroup,
        AnsysElementsGroup,
        AnsysFacesGroup,
    )

    # Ansys Constraints
    from .model.constraints import (
        AnsysTieConstraint,
    )

    # Ansys release
    from .model.releases import (
        AnsysBeamEndPinRelease,
    )

    # Ansys Boundary Conditions
    from .model.bcs import (
        AnsysFixedBC,
        AnsysClampBCXX,
        AnsysClampBCYY,
        AnsysClampBCZZ,
        AnsysPinnedBC,
        AnsysRollerBCX,
        AnsysRollerBCXY,
        AnsysRollerBCXZ,
        AnsysRollerBCY,
        AnsysRollerBCYZ,
        AnsysRollerBCZ,
    )

    # Ansys Problem
    from .problem import AnsysProblem

    # Ansys Steps
    from .problem.steps import (
        AnsysModalAnalysis,
        AnsysComplexEigenValue,
        AnsysStaticStep,
        AnsysLinearStaticPerturbation,
        AnsysBucklingAnalysis,
        AnsysDynamicStep,
        AnsysQuasiStaticStep,
        AnsysDirectCyclicStep,
    )
    # Ansys Loads
    from .problem.loads import (
        AnsysPointLoad,
        AnsysLineLoad,
        AnsysAreaLoad,
        AnsysTributaryLoad,
        AnsysPrestressLoad,
        AnsysGravityLoad,
        AnsysHarmonicPointLoad,
        AnsysHarmonicPressureLoad,
    )

    # Ansys Displacements
    from .problem.displacements import (
        AnsysGeneralDisplacement,
    )

    # Ansys outputs
    from .problem.outputs import (
        AnsysFieldOutput,
        AnsysHistoryOutput,
    )

    # Ansys Results
    from .results import (
        AnsysResults
    )

    # Ansys Input File
    from .job import(
        AnsysInputFile,
        AnsysParametersFile,
    )

    @plugin(category='fea_backends')
    def register_backend():
        backend = compas_fea2.BACKENDS['ansys']

        backend[Model] = AnsysModel
        backend[DeformablePart] = AnsysPart
        backend[Node] = AnsysNode

        backend[MassElement] = AnsysMassElement
        backend[BeamElement] = AnsysBeamElement
        backend[TrussElement] = AnsysTrussElement
        backend[MembraneElement] = AnsysMembraneElement
        backend[ShellElement] = AnsysShellElement
        backend[_Element3D] = _AnsysElement3D
        backend[_Element3D] = _AnsysElement3D
        backend[_Element3D] = _AnsysElement3D

        backend[AngleSection] = AnsysAngleSection
        backend[BeamSection] = AnsysBeamSection
        backend[BoxSection] = AnsysBoxSection
        backend[CircularSection] = AnsysCircularSection
        backend[HexSection] = AnsysHexSection
        backend[ISection] = AnsysISection
        backend[MassSection] = AnsysMassSection
        backend[MembraneSection] = AnsysMembraneSection
        backend[PipeSection] = AnsysPipeSection
        backend[RectangularSection] = AnsysRectangularSection
        backend[ShellSection] = AnsysShellSection
        backend[SolidSection] = AnsysSolidSection
        backend[SpringSection] = AnsysSpringSection
        backend[StrutSection] = AnsysStrutSection
        backend[TieSection] = AnsysTieSection
        backend[TrapezoidalSection] = AnsysTrapezoidalSection
        backend[TrussSection] = AnsysTrussSection

        backend[ElasticIsotropic] = AnsysElasticIsotropic
        backend[ElasticOrthotropic] = AnsysElasticOrthotropic
        backend[ElasticPlastic] = AnsysElasticPlastic
        backend[Stiff] = AnsysStiff
        backend[UserMaterial] = AnsysUserMaterial
        backend[Concrete] = AnsysConcrete
        backend[ConcreteDamagedPlasticity] = AnsysConcreteDamagedPlasticity
        backend[ConcreteSmearedCrack] = AnsysConcreteSmearedCrack
        backend[Steel] = AnsysSteel

        backend[NodesGroup] = AnsysNodesGroup
        backend[ElementsGroup] = AnsysElementsGroup
        backend[FacesGroup] = AnsysFacesGroup


        backend[TieConstraint] = AnsysTieConstraint

        backend[BeamEndPinRelease] = AnsysBeamEndPinRelease

        backend[FixedBC] = AnsysFixedBC
        backend[ClampBCXX] = AnsysClampBCXX
        backend[ClampBCYY] = AnsysClampBCYY
        backend[ClampBCZZ] = AnsysClampBCZZ
        backend[PinnedBC] = AnsysPinnedBC
        backend[RollerBCX] = AnsysRollerBCX
        backend[RollerBCXY] = AnsysRollerBCXY
        backend[RollerBCXZ] = AnsysRollerBCXZ
        backend[RollerBCY] = AnsysRollerBCY
        backend[RollerBCYZ] = AnsysRollerBCYZ
        backend[RollerBCZ] = AnsysRollerBCZ

        backend[Problem] = AnsysProblem

        backend[ModalAnalysis] = AnsysModalAnalysis
        backend[ComplexEigenValue, StaticStep] = AnsysComplexEigenValue
        backend[StaticStep] = AnsysStaticStep
        backend[LinearStaticPerturbation] = AnsysLinearStaticPerturbation
        backend[BucklingAnalysis] = AnsysBucklingAnalysis
        backend[DynamicStep] = AnsysDynamicStep
        backend[QuasiStaticStep] = AnsysQuasiStaticStep
        backend[DirectCyclicStep] = AnsysDirectCyclicStep

        backend[GravityLoad] = AnsysGravityLoad
        backend[PointLoad] = AnsysPointLoad
        backend[LineLoad] = AnsysLineLoad
        backend[AreaLoad] = AnsysAreaLoad
        backend[TributaryLoad] = AnsysTributaryLoad
        backend[PrestressLoad] = AnsysPrestressLoad
        backend[HarmonicPointLoad] = AnsysHarmonicPointLoad
        backend[HarmonicPressureLoad] = AnsysHarmonicPressureLoad

        backend[GeneralDisplacement] = AnsysGeneralDisplacement

        backend[FieldOutput] = AnsysFieldOutput
        backend[HistoryOutput] = AnsysHistoryOutput

        backend[Results] = AnsysResults

        backend[InputFile] = AnsysInputFile
        backend[ParametersFile] = AnsysParametersFile

        print('Ansys implementations registered...')
except:
    raise ErrorDuringImport()
