import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.math.RoundingMode;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import javafx.util.Pair;

public class Main {

    private static final String COLUMN_NAMES_DELIMITER = ",";
    private static final String COLUMN_VALUES_DELIMITER = " ";

    // example data had 10 digits after decimal point
    private static final DecimalFormat df = new DecimalFormat("#.##########");
    {
        df.setRoundingMode(RoundingMode.CEILING);
    }
    // humidity is missing because it is already "normalized" - between 0 and 1
    private static final List<String> COLUMNS_TO_NORMALIZE = Arrays.asList("temperature", "windSpeed", "precipIntensity", "p1", "p2");

    public static void main(String[] args) throws IOException {
        List<List<String>> records = new ArrayList<>();
        try (BufferedReader br = new BufferedReader(new FileReader(args[0]))) {
            records.add(Arrays.asList(br.readLine().split(COLUMN_NAMES_DELIMITER)));
            String line;
            while ((line = br.readLine()) != null) {
                String[] values = line.split(COLUMN_VALUES_DELIMITER);
                records.add(Arrays.asList(values));
            }
        }

        List<String> columns = records.get(0);
        List<Integer> indexesOfColumnToNormalize = columns.stream()
                .filter(COLUMNS_TO_NORMALIZE::contains)
                .map(columns::indexOf)
                .collect(Collectors.toList());

        System.out.println(indexesOfColumnToNormalize);
        // left is min, right is max
        Map<Integer, Pair<Double, Double>> columnIndexToMinMaxPair = new HashMap<>();
        for (Integer indexOfColumnToNormalize : indexesOfColumnToNormalize) {
            double min = Double.MAX_VALUE;
            double max = Double.MIN_VALUE;
            for (int i = 1 /*skip column names*/; i < records.size(); i++) {
                List<String> record = records.get(i);

                // missing data for column, skip for calculating min and max
                if ("".equals(record.get(indexOfColumnToNormalize))) {
                    continue;
                }

                double temperature = Double.valueOf(record.get(indexOfColumnToNormalize));
                if (min > temperature) {
                    min = temperature;
                }

                if (max < temperature) {
                    max = temperature;
                }
            }

            columnIndexToMinMaxPair.put(indexOfColumnToNormalize, new Pair<>(min, max));
        }

        System.out.println(columnIndexToMinMaxPair);

        List<String> normalizedRecords = new ArrayList<>();
        for (int i = 1; i < records.size(); i++) {
            List<String> record = records.get(i);
            // skip records without missing any column value
            if (record.stream().anyMatch(""::equals)) {
                continue;
            }

            List<String> normalizedRecord = new ArrayList<>();
            for (int j = 0; j < record.size(); j++) {
                if (!columnIndexToMinMaxPair.containsKey(j)) {
                    normalizedRecord.add(df.format(Double.valueOf(record.get(j))));
                } else {
                    double min = columnIndexToMinMaxPair.get(j).getKey();
                    double max = columnIndexToMinMaxPair.get(j).getValue();

                    double normalizedValue = (Double.valueOf(record.get(j)) - min) / (max - min);
                    normalizedRecord.add(df.format((normalizedValue)));
                }
            }

            normalizedRecords.add(
                    normalizedRecord.stream()
                            .collect(Collectors.joining(" ", "", ""))
            );
        }

        // return columns
        normalizedRecords.add(0,
                columns.stream().collect(Collectors.joining(" ", "", "")));

        // expects file doesn't have extension :D
        String normalizedFilePath = args[0] + "-normalized";

        Charset utf8 = StandardCharsets.UTF_8;
        Files.write(Paths.get(normalizedFilePath), normalizedRecords, utf8);
    }
}
