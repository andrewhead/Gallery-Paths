LC = [
	164.111415943, 131.087181832, 111.871056241;
	159.095167653, 125.382149901, 112.516272189;
	169.998347107, 128.253553719, 107.548429752;
	175.149585799, 129.893964497, 114.317633136;
	162.760541705, 120.905817175, 105.730686365;
	175.175308642, 128.311111111, 106.719506173;
	137.35654321, 96.6350617284, 79.9669135802;
	134.932281394, 93.9237343853, 72.3017751479;
	128.732302201, 89.4788816181, 72.5990481856;
];
DC = [
	54.811723886, 38.2689919649, 40.1364134405;
	46.2230935641, 28.2637912385, 35.3243645214;
	54.9732510288, 37.4420438957, 38.3456790123;
	60.9924557752, 42.8280437045, 48.6043184183;
	52.8138271605, 36.9412345679, 38.3051851852;
	48.7313580247, 31.9609876543, 35.815308642;
	47.9544753086, 33.962962963, 35.9012345679;
	52.942800789, 36.9191321499, 40.2018408941;
	47.9474030243, 32.1584483892, 37.1374095989;
];
hold('off')
scatter3(LC(:,1), LC(:,2), LC(:,3), 'ro')
hold('on')
scatter3(DC(:,1), DC(:,2), DC(:,3), 'bx')
xlim([0, 255]); ylim([0, 255]); zlim([0, 255]);